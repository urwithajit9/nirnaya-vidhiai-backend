from django.db import connection
from sentence_transformers import SentenceTransformer


class VectorService:
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            cls._model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
        return cls._model

    def find_context(self, query: str, limit: int = 5):
        model = self.get_model()
        embedding = model.encode(query).tolist()

        with connection.cursor() as cur:
            cur.execute(
                """
                SELECT content, doc_level
                FROM knowledge_base
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                (embedding, limit),
            )

            rows = cur.fetchall()
            return [{"content": r[0], "doc_level": r[1]} for r in rows]
