"""
Configuration module for the web scraper package.
"""
from .settings import (
    OPENAI_API_KEY,
    OPENAI_EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    MAX_RETRIES,
    RETRY_DELAY
)

__all__ = [
    'OPENAI_API_KEY',
    'OPENAI_EMBEDDING_MODEL',
    'CHUNK_SIZE',
    'CHUNK_OVERLAP',
    'MAX_RETRIES',
    'RETRY_DELAY'
]
