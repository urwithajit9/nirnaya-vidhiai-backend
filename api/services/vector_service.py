# from django.db import connection
# from sentence_transformers import SentenceTransformer


# class VectorService:
#     _model = None

#     @classmethod
#     def get_model(cls):
#         if cls._model is None:
#             cls._model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
#         return cls._model

#     def find_context(self, query: str, limit: int = 5):
#         model = self.get_model()
#         embedding = model.encode(query).tolist()

#         with connection.cursor() as cur:
#             cur.execute(
#                 """
#                 SELECT content, doc_level
#                 FROM knowledge_base
#                 ORDER BY embedding <=> %s::vector
#                 LIMIT %s
#                 """,
#                 (embedding, limit),
#             )

#             rows = cur.fetchall()
#             return [{"content": r[0], "doc_level": r[1]} for r in rows]

from django.db import connection
from sentence_transformers import SentenceTransformer
from typing import List, Dict
from datetime import date


class VectorService:
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            cls._model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
        return cls._model

    def embed(self, text: str) -> List[float]:
        model = self.get_model()
        return model.encode(text).tolist()


    def find_context(self, query: str, limit: int = 5) -> List[Dict]:
        embedding = self.embed(query)
        similarity_threshold = 0.75

        sql = """
            WITH query_embedding AS (
                SELECT %s::vector AS qvec
            )
            SELECT kb.id, kb.content, kb.doc_level, kb.metadata,
                kb.embedding <=> q.qvec AS distance
            FROM knowledge_base kb, query_embedding q
            WHERE (kb.effective_date IS NULL OR kb.effective_date <= %s)
            AND kb.embedding <=> q.qvec < %s
            ORDER BY kb.embedding <=> q.qvec
            LIMIT %s
        """

        params = [embedding, date.today(), similarity_threshold, limit]

        with connection.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()

        return [
            {
                "id": r[0],
                "content": r[1],
                "doc_level": r[2],
                "metadata": r[3],
                "distance": r[4],
            }
            for r in rows
        ]
