import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Set
from urllib.parse import urljoin, urlparse

import nltk
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
from ratelimit import limits, sleep_and_retry
from transformers import AutoTokenizer


class PageScraper:
    def __init__(self, max_depth: int = 2, max_pages: int = 100):
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.visited_urls: Set[str] = set()
        # Download required NLTK data
        nltk.download('punkt')

    def get_token_count(text, model_name="gpt-3.5-turbo"):
        """Count tokens for GPT models"""
        """Count tokens for GPT models"""
        try:
            # Ensure text is a string
            text = str(text).strip()

            # Handle empty text
            if not text:
                return 0

            tokenizer = AutoTokenizer.from_pretrained("gpt2")
            # Convert to string type explicitly and encode
            tokens = tokenizer.encode(str(text), add_special_tokens=True)
            return len(tokens)
        except Exception as e:
            print(f"Error in token counting: {str(e)}")
            return 0

    def create_semantic_chunks(self, text, max_tokens=1000, overlap_sentences=2):
        """Create overlapping semantic chunks based on sentences"""
        # Split into sentences
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = []
        current_token_count = 0

        for i in range(len(sentences)):
            sentence = sentences[i]
            sentence_tokens = self.get_token_count(sentence)

            # If adding this sentence would exceed max tokens, save chunk and start new one
            if current_token_count + sentence_tokens > max_tokens and current_chunk:
                chunks.append(" ".join(current_chunk))
                # Keep last N sentences for overlap
                current_chunk = current_chunk[-overlap_sentences:] if overlap_sentences > 0 else []
                current_token_count = sum(self.get_token_count(s) for s in current_chunk)

            current_chunk.append(sentence)
            current_token_count += sentence_tokens

        # Add the last chunk if it's not empty
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    @sleep_and_retry
    @limits(calls=10, period=1)  # Rate limiting: 10 requests per second
    def _fetch_page(self, url: str) -> str:
        """Fetch page content with rate limiting and retries."""
        response = requests.get(url, headers={'User-Agent': 'Custom Web Scraper 1.0'})
        response.raise_for_status()
        return response.text

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract and normalize all clickable links from the page."""
        links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(base_url, href)
            if self._is_valid_url(full_url, base_url):
                links.append(full_url)
        return links

    def _is_valid_url(self, url: str, base_url: str) -> bool:
        """Check if URL is valid and belongs to the same domain."""
        try:
            base_domain = urlparse(base_url).netloc
            url_domain = urlparse(url).netloc
            return base_domain == url_domain
        except Exception:
            return False

    def scrape(self, start_url: str) -> List[Dict]:
        """Scrape website content starting from the given URL."""
        pages_data = []
        current_depth = 0
        urls_to_visit = [(start_url, current_depth)]

        with ThreadPoolExecutor(max_workers=5) as executor:
            while urls_to_visit and len(pages_data) < self.max_pages:
                current_url, depth = urls_to_visit.pop(0)

                if current_url in self.visited_urls or depth > self.max_depth:
                    continue

                try:
                    html_content = self._fetch_page(current_url)
                    soup = BeautifulSoup(html_content, 'html.parser')
                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.decompose()

                    # Get text content
                    text = soup.get_text(separator=" ", strip=True)

                    # Create semantic chunks
                    chunks = self.create_semantic_chunks(text)

                    links = self._extract_links(soup, current_url)

                    # Store chunks with metadata
                    for i, chunk in enumerate(chunks):
                        pages_data.append({
                            'url': current_url,
                            'chunk_id': i,
                            'content': chunk,
                            'links': links,
                            'token_count': self.get_token_count(chunk)
                        })
                    self.visited_urls.add(current_url)

                    # Add new links to visit
                    if depth < self.max_depth:
                        urls_to_visit.extend([(url, depth + 1) for url in links])

                except Exception as e:
                    logging.error(f"Error scraping {current_url}: {str(e)}")
                    continue

        return pages_data
