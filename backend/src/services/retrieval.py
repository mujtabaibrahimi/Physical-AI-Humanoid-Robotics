"""
RAG Retrieval Service
Retrieves relevant content from Qdrant vector database
"""

from typing import List, Optional, Dict, Any
import logging

from ..models.config import settings

logger = logging.getLogger(__name__)


class RetrievalService:
    """Service for RAG retrieval from Qdrant (lazy initialization)"""

    _instance = None
    _client = None
    _initialized = False
    _embedding_service = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _ensure_initialized(self):
        """Lazy initialize Qdrant client"""
        if self._initialized:
            return

        if not settings.is_qdrant_configured:
            logger.warning("Qdrant not configured - retrieval will return empty results")
            self._initialized = True
            return

        try:
            from qdrant_client import QdrantClient
            from qdrant_client.models import Distance, VectorParams

            self._client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key
            )
            self._ensure_collection()
            self._initialized = True
            logger.info("Qdrant client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant: {e}")
            self._initialized = True  # Mark as initialized to avoid retries

    def _get_embedding_service(self):
        """Lazy get embedding service"""
        if self._embedding_service is None:
            from .embedding import get_embedding_service
            self._embedding_service = get_embedding_service()
        return self._embedding_service

    def _ensure_collection(self):
        """Create collection if it doesn't exist"""
        if not self._client:
            return

        from qdrant_client.models import Distance, VectorParams

        collections = self._client.get_collections().collections
        collection_names = [c.name for c in collections]

        if settings.qdrant_collection_name not in collection_names:
            logger.info(f"Creating collection: {settings.qdrant_collection_name}")
            self._client.create_collection(
                collection_name=settings.qdrant_collection_name,
                vectors_config=VectorParams(
                    size=self._get_embedding_service().dimension,
                    distance=Distance.COSINE
                )
            )
            logger.info("Collection created successfully")

    @property
    def is_available(self) -> bool:
        """Check if retrieval service is configured"""
        self._ensure_initialized()
        return self._client is not None

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
        chapter_filter: Optional[str] = None,
        score_threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant content chunks for a query.
        """
        self._ensure_initialized()

        if not self._client:
            logger.warning("Qdrant not available - returning empty results")
            return []

        try:
            from qdrant_client.models import Filter, FieldCondition, MatchValue

            query_vector = self._get_embedding_service().embed_text(query)

            filter_condition = None
            if chapter_filter:
                filter_condition = Filter(
                    must=[
                        FieldCondition(key="chapter", match=MatchValue(value=chapter_filter))
                    ]
                )

            results = self._client.query_points(
                collection_name=settings.qdrant_collection_name,
                query=query_vector,
                limit=top_k,
                query_filter=filter_condition,
                score_threshold=score_threshold
            )

            retrieved_chunks = []
            for result in results.points:
                retrieved_chunks.append({
                    "content": result.payload.get("content", ""),
                    "chapter": result.payload.get("chapter", ""),
                    "section": result.payload.get("section", ""),
                    "score": result.score
                })

            return retrieved_chunks
        except Exception as e:
            logger.error(f"Retrieval failed: {e}")
            return []

    def retrieve_by_selection(
        self,
        selected_text: str,
        score_threshold: float = 0.5
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve the exact chunk matching user-selected text.
        """
        self._ensure_initialized()

        if not self._client:
            return None

        try:
            query_vector = self._get_embedding_service().embed_text(selected_text)

            results = self._client.query_points(
                collection_name=settings.qdrant_collection_name,
                query=query_vector,
                limit=1,
                score_threshold=score_threshold
            )

            if results.points and results.points[0].score >= score_threshold:
                result = results.points[0]
                return {
                    "content": result.payload.get("content", ""),
                    "chapter": result.payload.get("chapter", ""),
                    "section": result.payload.get("section", ""),
                    "score": result.score
                }

            return None
        except Exception as e:
            logger.error(f"Selection retrieval failed: {e}")
            return None

    def index_chunk(
        self,
        chunk_id: str,
        content: str,
        chapter: str,
        section: str
    ) -> bool:
        """Index a single content chunk"""
        self._ensure_initialized()

        if not self._client:
            logger.error("Cannot index - Qdrant not configured")
            return False

        try:
            from qdrant_client.models import PointStruct

            vector = self._get_embedding_service().embed_text(content)
            point = PointStruct(
                id=hash(chunk_id) % (2**63),
                vector=vector,
                payload={
                    "content": content,
                    "chapter": chapter,
                    "section": section,
                    "chunk_id": chunk_id
                }
            )
            self._client.upsert(
                collection_name=settings.qdrant_collection_name,
                points=[point]
            )
            return True
        except Exception as e:
            logger.error(f"Failed to index chunk {chunk_id}: {e}")
            return False

    def get_collection_info(self) -> Dict[str, Any]:
        """Get collection statistics"""
        self._ensure_initialized()

        if not self._client:
            return {"status": "not_configured"}

        try:
            info = self._client.get_collection(settings.qdrant_collection_name)
            return {
                "name": settings.qdrant_collection_name,
                "points_count": getattr(info, 'points_count', 0),
                "status": "ready"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}


def get_retrieval_service() -> RetrievalService:
    """Get or create retrieval service instance"""
    return RetrievalService()
