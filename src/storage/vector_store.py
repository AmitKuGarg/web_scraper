import json
import os
from typing import List, Dict

import faiss
import numpy as np

from src.embeddings.openai_embeddings import OpenAIEmbeddings


class VectorStore:
    def __init__(self, embedding_dim: int = 3072):  # text-embedding-3-large dimension
        self.embeddings = OpenAIEmbeddings()
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.documents: List[Dict] = []

    def add_documents(self, documents: List[Dict]):
        """Add documents to the vector store."""
        for doc in documents:
            # Create embedding for the document content
            embedding = self.embeddings.create_embedding(doc['content'])

            # Add to FAISS index
            self.index.add(np.array([embedding], dtype=np.float32))

            # Store document
            self.documents.append({
                'url': doc['url'],
                'chunk_id': doc['chunk_id'],
                'content': doc['content'],
                'links': doc['links'],
                'token_count': doc['token_count']
            })

    def search(self, query: str, k: int = 5) -> List[Dict]:
        """Search for similar documents using the query."""
        # Create query embedding
        query_embedding = self.embeddings.create_embedding(query)

        # Search in FAISS index
        distances, indices = self.index.search(
            np.array([query_embedding], dtype=np.float32),
            k
        )

        # Return matched documents
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx != -1:  # Valid index
                doc = self.documents[idx]
                results.append({
                    'url': doc['url'],
                    'chunk_id': doc['chunk_id'],
                    'content': doc['content'],
                    'links': doc['links'],
                    'token_count': doc['token_count'],
                    'distance': float(distance)
                })

        return results

    def save(self, directory: str):
        """Save vector store to disk."""
        os.makedirs(directory, exist_ok=True)

        # Save FAISS index
        faiss.write_index(self.index, os.path.join(directory, 'index.faiss'))

        # Save documents
        with open(os.path.join(directory, 'documents.json'), 'w') as f:
            json.dump(self.documents, f)

    def load(self, directory: str):
        """Load vector store from disk."""
        # Load FAISS index
        self.index = faiss.read_index(os.path.join(directory, 'index.faiss'))

        # Load documents
        with open(os.path.join(directory, 'documents.json'), 'r') as f:
            self.documents = json.load(f)
