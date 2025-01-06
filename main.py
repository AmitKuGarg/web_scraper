import argparse
import logging

from src.scraper.page_scraper import PageScraper
from src.storage.vector_store import VectorStore


def main():
    parser = argparse.ArgumentParser(description='Web Scraper and Vector Store')
    parser.add_argument('url', help='Starting URL to scrape')
    parser.add_argument('--depth', type=int, default=2, help='Maximum crawl depth')
    parser.add_argument('--max-pages', type=int, default=2, help='Maximum pages to scrape')
    parser.add_argument('--save-dir', default='vector_store', help='Directory to save vector store')

    args = parser.parse_args()

    # Initialize scraper and vector store
    scraper = PageScraper(max_depth=args.depth, max_pages=args.max_pages)
    vector_store = VectorStore()
    try:
        # Load vector store if exists
        vector_store.load(args.save_dir)
    except Exception as e:
        logging.warning("Vector store not found, starting")
        logging.debug(str(e))
    try:
        # Scrape website
        logging.info(f"Starting scrape of {args.url}")
        pages_data = scraper.scrape(args.url)

        # Add to vector store
        logging.info("Adding documents to vector store")
        vector_store.add_documents(pages_data)
        # Save vector store
        logging.info(f"Saving vector store to {args.save_dir}")
        vector_store.save(args.save_dir)

        logging.info("Process completed successfully")

    except Exception as e:
        logging.error(f"Error during processing: {str(e)}")
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()