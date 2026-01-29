"""
Database Migration Script
Create Neon PostgreSQL schema for query logs and metadata
"""

import psycopg
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.config import settings


def create_schema():
    """Create database schema with query_logs and metadata tables"""

    # SQL schema from research.md
    schema_sql = """
    -- Query logs table
    CREATE TABLE IF NOT EXISTS query_logs (
        query_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        session_id VARCHAR(64) NOT NULL,
        query_text VARCHAR(500) NOT NULL CHECK (length(query_text) >= 5),
        response_text TEXT NOT NULL,
        citations JSONB NOT NULL,
        retrieved_chunks JSONB NOT NULL,
        response_time_ms INTEGER NOT NULL CHECK (response_time_ms > 0),
        cache_hit BOOLEAN NOT NULL DEFAULT false,
        user_ip_hash VARCHAR(64) NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW()
    );

    -- Indexes for query performance
    CREATE INDEX IF NOT EXISTS idx_query_logs_session_id ON query_logs(session_id);
    CREATE INDEX IF NOT EXISTS idx_query_logs_created_at ON query_logs(created_at DESC);
    CREATE INDEX IF NOT EXISTS idx_query_logs_cache_hit ON query_logs(cache_hit);

    -- Metadata table (key-value store for system config)
    CREATE TABLE IF NOT EXISTS metadata (
        key VARCHAR(255) PRIMARY KEY,
        value JSONB NOT NULL,
        updated_at TIMESTAMP NOT NULL DEFAULT NOW()
    );

    -- Insert initial metadata
    INSERT INTO metadata (key, value) VALUES
    ('index_version', '{"version": "1.0.0", "indexed_at": null}'),
    ('total_chunks', '{"count": 0}'),
    ('last_content_update', '{"timestamp": null, "chapters_updated": []}')
    ON CONFLICT (key) DO NOTHING;
    """

    try:
        # Connect to Neon PostgreSQL
        print(f"Connecting to Neon PostgreSQL...")
        with psycopg.connect(settings.neon_database_url) as conn:
            with conn.cursor() as cur:
                # Execute schema creation
                cur.execute(schema_sql)
                conn.commit()
                print("✓ Schema created successfully")

                # Verify tables exist
                cur.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name IN ('query_logs', 'metadata')
                    ORDER BY table_name;
                """)
                tables = cur.fetchall()
                print(f"✓ Tables created: {[t[0] for t in tables]}")

    except Exception as e:
        print(f"✗ Error creating schema: {e}")
        sys.exit(1)


if __name__ == "__main__":
    print("Starting database migration...")
    create_schema()
    print("Migration complete!")
