import numpy as np
from openai import OpenAI

from src.config.settings import OPENAI_API_KEY, OPENAI_EMBEDDING_MODEL


class OpenAIEmbeddings:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_EMBEDDING_MODEL

    def create_embedding(self, text: str) -> np.ndarray:
        """Create embedding for the given text."""
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return np.array(response.data[0].embedding, dtype=np.float32)
