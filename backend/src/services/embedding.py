"""
Embedding Service
Generates vector embeddings using sentence-transformers
"""

from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating text embeddings (lazy initialization)"""

    _instance = None
    _model = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _ensure_initialized(self):
        """Lazy load the model on first use"""
        if not self._initialized:
            try:
                from sentence_transformers import SentenceTransformer
                logger.info("Loading embedding model: all-MiniLM-L6-v2")
                self._model = SentenceTransformer('all-MiniLM-L6-v2')
                self._initialized = True
                logger.info("Embedding model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load embedding model: {e}")
                raise

    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        self._ensure_initialized()
        embedding = self._model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        self._ensure_initialized()
        embeddings = self._model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()

    @property
    def dimension(self) -> int:
        """Return embedding dimension"""
        return 384  # all-MiniLM-L6-v2 dimension

    @property
    def is_available(self) -> bool:
        """Check if model can be loaded"""
        try:
            self._ensure_initialized()
            return True
        except:
            return False


def get_embedding_service() -> EmbeddingService:
    """Get or create embedding service instance"""
    return EmbeddingService()
