"""
Chat Router
API endpoints for RAG chatbot following strict grounding policies
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
import logging

from ...services.retrieval import get_retrieval_service
from ...services.llm import get_llm_service, REFUSAL_NO_CONTENT, REFUSAL_NO_TRANSLATION

logger = logging.getLogger(__name__)

router = APIRouter()


# Request/Response Models

class ChatRequest(BaseModel):
    """Chat query request"""
    query: str = Field(..., min_length=1, max_length=500)
    chapter_filter: Optional[str] = Field(None, description="Scope to specific chapter")
    selected_text: Optional[str] = Field(None, description="User-highlighted text for scoped query")


class TranslateRequest(BaseModel):
    """Translation request"""
    content: str = Field(..., min_length=1, description="Content to translate (must be from retrieval)")
    target_language: str = Field(..., pattern="^(pashto|dari)$", description="Target language: pashto or dari")
    source_chapter: Optional[str] = Field(None, description="Source chapter for verification")


class ChatResponse(BaseModel):
    """Chat response"""
    response: str
    sources: List[str] = []
    grounded: bool = True


class TranslateResponse(BaseModel):
    """Translation response"""
    original: str
    translated: str
    target_language: str


# Endpoints

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat query with RAG retrieval.
    """
    retrieval_service = get_retrieval_service()
    llm_service = get_llm_service()

    try:
        # Scoped query: user selected specific text
        if request.selected_text:
            matched_chunk = retrieval_service.retrieve_by_selection(
                selected_text=request.selected_text
            )

            if not matched_chunk:
                return ChatResponse(
                    response=REFUSAL_NO_CONTENT,
                    sources=[],
                    grounded=False
                )

            response = llm_service.generate_grounded_response(
                query=request.query,
                retrieved_chunks=[matched_chunk],
                selected_text=request.selected_text
            )

            return ChatResponse(
                response=response,
                sources=[matched_chunk["chapter"]],
                grounded=True
            )

        # Global or chapter-scoped retrieval
        retrieved_chunks = retrieval_service.retrieve(
            query=request.query,
            top_k=3,
            chapter_filter=request.chapter_filter
        )

        if not retrieved_chunks:
            return ChatResponse(
                response=REFUSAL_NO_CONTENT,
                sources=[],
                grounded=False
            )

        response = llm_service.generate_grounded_response(
            query=request.query,
            retrieved_chunks=retrieved_chunks
        )

        # Extract unique sources
        sources = list(set(chunk["chapter"] for chunk in retrieved_chunks))

        return ChatResponse(
            response=response,
            sources=sources,
            grounded=True
        )

    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/translate", response_model=TranslateResponse)
async def translate(request: TranslateRequest):
    """
    Translate retrieved content to Pashto or Dari.
    """
    retrieval_service = get_retrieval_service()
    llm_service = get_llm_service()

    try:
        # Validate content exists in our index (prevent arbitrary translation)
        if request.source_chapter:
            matched = retrieval_service.retrieve_by_selection(
                selected_text=request.content,
                score_threshold=0.8
            )
            if not matched:
                return TranslateResponse(
                    original=request.content,
                    translated=REFUSAL_NO_TRANSLATION,
                    target_language=request.target_language
                )

        translated = llm_service.translate_content(
            content=request.content,
            target_language=request.target_language
        )

        return TranslateResponse(
            original=request.content,
            translated=translated,
            target_language=request.target_language
        )

    except Exception as e:
        logger.error(f"Translation endpoint error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/status")
async def status():
    """Get RAG system status"""
    retrieval_service = get_retrieval_service()
    llm_service = get_llm_service()

    try:
        collection_info = retrieval_service.get_collection_info()
        return {
            "status": "operational",
            "qdrant_configured": retrieval_service.is_available,
            "groq_configured": llm_service.is_available,
            "collection": collection_info,
            "embedding_model": "all-MiniLM-L6-v2"
        }
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        return {
            "status": "degraded",
            "error": str(e)
        }
