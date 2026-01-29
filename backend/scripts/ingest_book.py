"""
Book Content Ingestion Script
Chunks and embeds book content into Qdrant vector database
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from src.services.embedding import get_embedding_service
from src.services.retrieval import get_retrieval_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
DOCS_PATH = Path(__file__).parent.parent.parent / "frontend" / "docs"
CHUNK_SIZE = 500  # Target words per chunk
CHUNK_OVERLAP = 50  # Words overlap between chunks


def extract_sections(content: str) -> List[Dict[str, str]]:
    """Extract sections from markdown content"""
    sections = []

    # Split by headers (## or ###)
    pattern = r'^(#{2,3})\s+(.+?)$'
    parts = re.split(pattern, content, flags=re.MULTILINE)

    current_section = "Introduction"
    current_content = []

    i = 0
    while i < len(parts):
        part = parts[i].strip()

        if part.startswith('#'):
            # Save previous section
            if current_content:
                sections.append({
                    "section": current_section,
                    "content": "\n".join(current_content)
                })
                current_content = []

            # Get section title
            if i + 1 < len(parts):
                current_section = parts[i + 1].strip()
                i += 2
            else:
                i += 1
        else:
            if part:
                current_content.append(part)
            i += 1

    # Save final section
    if current_content:
        sections.append({
            "section": current_section,
            "content": "\n".join(current_content)
        })

    return sections


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Split text into overlapping chunks by word count"""
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])

        # Only add non-empty chunks
        if chunk.strip():
            chunks.append(chunk)

        start = end - overlap

        # Prevent infinite loop
        if start >= len(words) - overlap:
            break

    return chunks


def process_chapter(file_path: Path) -> List[Dict]:
    """Process a single chapter file"""
    logger.info(f"Processing: {file_path.name}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract chapter name from first line
    first_line = content.split('\n')[0]
    chapter_name = first_line.replace('#', '').strip()
    chapter_id = file_path.stem  # e.g., "chapter-01"

    # Extract sections
    sections = extract_sections(content)

    chunks = []
    for section in sections:
        section_chunks = chunk_text(section["content"])

        for i, chunk_text_content in enumerate(section_chunks):
            chunk_id = f"{chapter_id}_{section['section']}_{i}"
            chunks.append({
                "chunk_id": chunk_id,
                "content": chunk_text_content,
                "chapter": chapter_id,
                "chapter_name": chapter_name,
                "section": section["section"]
            })

    logger.info(f"  - Extracted {len(chunks)} chunks from {len(sections)} sections")
    return chunks


def ingest_all_chapters():
    """Ingest all chapter files into Qdrant"""
    retrieval_service = get_retrieval_service()

    logger.info("=" * 50)
    logger.info("Book Content Ingestion")
    logger.info("=" * 50)

    # Find all chapter files
    chapter_files = sorted(DOCS_PATH.glob("chapter-*.md"))

    if not chapter_files:
        logger.error(f"No chapter files found in {DOCS_PATH}")
        return

    logger.info(f"Found {len(chapter_files)} chapter files")

    all_chunks = []
    for chapter_file in chapter_files:
        chunks = process_chapter(chapter_file)
        all_chunks.extend(chunks)

    logger.info(f"\nTotal chunks to index: {len(all_chunks)}")

    # Index chunks
    logger.info("\nIndexing chunks into Qdrant...")
    success_count = 0

    for chunk in all_chunks:
        success = retrieval_service.index_chunk(
            chunk_id=chunk["chunk_id"],
            content=chunk["content"],
            chapter=chunk["chapter"],
            section=chunk["section"]
        )
        if success:
            success_count += 1

    logger.info(f"\nIndexed {success_count}/{len(all_chunks)} chunks successfully")

    # Verify
    info = retrieval_service.get_collection_info()
    logger.info(f"\nCollection status: {info}")


def test_retrieval():
    """Test retrieval with sample queries"""
    retrieval_service = get_retrieval_service()

    logger.info("\n" + "=" * 50)
    logger.info("Testing Retrieval")
    logger.info("=" * 50)

    test_queries = [
        "What is Physical AI?",
        "How do robots use sensors?",
        "What is ROS 2?"
    ]

    for query in test_queries:
        logger.info(f"\nQuery: {query}")
        results = retrieval_service.retrieve(query, top_k=2)

        for i, result in enumerate(results):
            logger.info(f"  Result {i+1} (score: {result['score']:.3f}):")
            logger.info(f"    Chapter: {result['chapter']}")
            logger.info(f"    Section: {result['section']}")
            logger.info(f"    Content: {result['content'][:100]}...")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ingest book content into Qdrant")
    parser.add_argument("--test", action="store_true", help="Run test queries after ingestion")
    args = parser.parse_args()

    ingest_all_chapters()

    if args.test:
        test_retrieval()
