"""
Input Validation Utility
SQL injection, XSS, and prompt injection prevention
"""

import re
from typing import Optional


class ValidationError(Exception):
    """Custom validation error"""
    pass


def sanitize_query_text(query: str) -> str:
    """
    Sanitize user query text to prevent injection attacks

    Args:
        query: Raw user query

    Returns:
        Sanitized query text

    Raises:
        ValidationError: If query contains malicious patterns
    """
    # Check length
    if len(query) < 5:
        raise ValidationError("Query must be at least 5 characters")
    if len(query) > 500:
        raise ValidationError("Query cannot exceed 500 characters")

    # Remove HTML tags
    query = re.sub(r'<[^>]+>', '', query)

    # Check for SQL injection patterns
    sql_patterns = [
        r"(?i)(union\s+select)",
        r"(?i)(drop\s+table)",
        r"(?i)(insert\s+into)",
        r"(?i)(delete\s+from)",
        r"(?i)(update\s+.+set)",
        r"--",
        r";--",
        r"';",
    ]
    for pattern in sql_patterns:
        if re.search(pattern, query):
            raise ValidationError("Query contains invalid characters")

    # Check for script tags (XSS)
    if "<script" in query.lower() or "javascript:" in query.lower():
        raise ValidationError("Query contains invalid characters")

    # Check for prompt injection attempts
    prompt_injection_patterns = [
        r"(?i)(ignore\s+(previous|above)\s+instructions?)",
        r"(?i)(system\s*:)",
        r"(?i)(assistant\s*:)",
        r"```",  # Code blocks
    ]
    for pattern in prompt_injection_patterns:
        if re.search(pattern, query):
            raise ValidationError("Query contains invalid characters")

    return query.strip()


def validate_session_id(session_id: str) -> bool:
    """
    Validate session ID format

    Args:
        session_id: Session identifier

    Returns:
        True if valid format

    Raises:
        ValidationError: If invalid format
    """
    # Expected format: ses_{timestamp}_{random_8_chars}
    pattern = r"^ses_\d+_[a-z0-9]{8}$"
    if not re.match(pattern, session_id):
        raise ValidationError("Invalid session ID format")
    return True


def validate_chapter_number(chapter: int) -> bool:
    """
    Validate chapter number is within valid range

    Args:
        chapter: Chapter number

    Returns:
        True if valid

    Raises:
        ValidationError: If invalid
    """
    if not 1 <= chapter <= 6:
        raise ValidationError("Chapter number must be between 1 and 6")
    return True
