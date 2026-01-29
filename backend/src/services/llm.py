"""
LLM Service
Handles chat completions using Groq API with strict RAG grounding
"""

from typing import List, Dict, Optional
import logging

from ..models.config import settings

logger = logging.getLogger(__name__)

# Refusal messages per policy
REFUSAL_NO_CONTENT = "The answer is not available in the selected content."
REFUSAL_NO_TRANSLATION = "The requested content is not available for translation."


class LLMService:
    """Service for grounded LLM responses using Groq (lazy initialization)"""

    _instance = None
    _client = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _ensure_initialized(self):
        """Lazy initialize Groq client"""
        if self._initialized:
            return

        if not settings.is_groq_configured:
            logger.warning("Groq not configured - LLM responses will use fallback")
            self._initialized = True
            return

        try:
            from groq import Groq
            self._client = Groq(api_key=settings.groq_api_key)
            self._initialized = True
            logger.info("Groq client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Groq: {e}")
            self._initialized = True

    @property
    def is_available(self) -> bool:
        """Check if LLM service is configured"""
        self._ensure_initialized()
        return self._client is not None

    def generate_grounded_response(
        self,
        query: str,
        retrieved_chunks: List[Dict],
        selected_text: Optional[str] = None
    ) -> str:
        """
        Generate response strictly grounded in retrieved content.
        """
        self._ensure_initialized()

        # No content retrieved - refuse per policy
        if not retrieved_chunks:
            return REFUSAL_NO_CONTENT

        # Build context from retrieved chunks
        if selected_text:
            context = selected_text
        else:
            context = "\n\n".join([
                f"[{chunk['chapter']} - {chunk['section']}]\n{chunk['content']}"
                for chunk in retrieved_chunks
            ])

        # If Groq not configured, return context summary
        if not self._client:
            return f"[Demo Mode - Groq not configured]\n\nBased on retrieved content:\n{context[:500]}..."

        system_prompt = """You are a technical assistant for a Physical AI and Humanoid Robotics textbook.

STRICT RULES:
1. Answer ONLY based on the provided context below
2. If the context does not contain information to answer the question, respond exactly: "The answer is not available in the selected content."
3. Do NOT add information beyond what is in the context
4. Do NOT make assumptions or inferences not supported by the context
5. Keep responses concise and technical
6. Cite the source chapter/section when relevant

CONTEXT:
{context}"""

        try:
            response = self._client.chat.completions.create(
                model=settings.groq_model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt.format(context=context)
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                max_tokens=settings.groq_max_tokens,
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return REFUSAL_NO_CONTENT

    def translate_content(
        self,
        content: str,
        target_language: str
    ) -> str:
        """
        Translate retrieved content to target language.
        """
        self._ensure_initialized()

        # Validate language per policy
        allowed_languages = ["pashto", "dari"]
        if target_language.lower() not in allowed_languages:
            return REFUSAL_NO_TRANSLATION

        # No content to translate
        if not content or not content.strip():
            return REFUSAL_NO_TRANSLATION

        # If Groq not configured
        if not self._client:
            return f"[Demo Mode - Translation to {target_language} not available without Groq API key]"

        language_names = {
            "pashto": "Pashto",
            "dari": "Dari (Afghan Persian)"
        }

        system_prompt = f"""You are a technical translator.

STRICT RULES:
1. Translate the following text to {language_names[target_language.lower()]}
2. Preserve the exact meaning - do NOT add explanations or summaries
3. Keep all technical terms, code identifiers, and proper nouns untranslated
4. Maintain the original paragraph and list structure
5. Do NOT add any commentary or clarifications

TEXT TO TRANSLATE:
{content}"""

        try:
            response = self._client.chat.completions.create(
                model=settings.groq_model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": f"Translate to {language_names[target_language.lower()]}"
                    }
                ],
                max_tokens=settings.groq_max_tokens * 2,
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return REFUSAL_NO_TRANSLATION


def get_llm_service() -> LLMService:
    """Get or create LLM service instance"""
    return LLMService()
