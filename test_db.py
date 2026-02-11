import os
import django
from django.db import connection

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()


def test_connection():
    try:
        with connection.cursor() as cursor:
            # 1. Check if we can connect
            cursor.execute("SELECT 1;")
            print("✅ Database Connection: SUCCESS")

            # 2. Check for pgvector extension
            cursor.execute("SELECT extname FROM pg_extension WHERE extname = 'vector';")
            if cursor.fetchone():
                print("✅ pgvector Extension: ENABLED")
            else:
                print(
                    "❌ pgvector Extension: NOT FOUND (Run 'CREATE EXTENSION vector;' in Supabase)"
                )

            # 3. Check for your ingested data
            cursor.execute("SELECT COUNT(*) FROM knowledge_base;")
            count = cursor.fetchone()[0]
            print(f"📊 Knowledge Base Chunks: {count}")

    except Exception as e:
        print(f"❌ Connection Failed: {e}")


if __name__ == "__main__":
    test_connection()
