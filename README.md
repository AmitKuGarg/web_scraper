# Web Scraper with OpenAI Vector Embeddings

A Python-based web scraper that extracts content from websites and creates vector embeddings using OpenAI's text-embedding-3-large model. The embeddings are stored in a local directory for efficient similarity search and retrieval.

## Features

- Web scraping with automatic content extraction
- Vector embeddings generation using OpenAI's text-embedding-3-large
- Local vector database storage
- Command-line interface for easy usage
- Configurable storage location

## Prerequisites

- Python 3.12 or higher
- OpenAI API key

## Installation

1. Clone the repository:
```bash
cd web_scraper
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
# Create a .env file and add your OpenAI API key
echo "OPENAI_API_KEY=your-api-key-here" > .env
```


## Usage

Run the scraper from the command line:

```bash
python main.py https://www.rsystems.com/ --save-dir=C:\learn\vector_store
```

### Arguments

-  The target URL to scrape (required)
- `--output`: Directory path where the vector database will be stored (required)
