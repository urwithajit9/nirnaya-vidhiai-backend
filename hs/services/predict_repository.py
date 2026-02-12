from django.db import connection
from typing import List, Dict


class HSPredictRepository:

    def hybrid_search(
        self, query: str, embedding: List[float], schedule_type: str, limit=10
    ):

        sql = """
        SELECT
            id,
            hs_code,
            description,
            chapter_num,
            policy,
            1 - (embedding <=> %s::vector) AS vector_score,
            ts_rank(
                to_tsvector('english', description),
                plainto_tsquery('english', %s)
            ) AS fts_score
        FROM itc_hs_master
        WHERE schedule_type = %s
        ORDER BY embedding <=> %s::vector
        LIMIT %s;
        """

        params = [embedding, query, schedule_type, embedding, limit]

        with connection.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()

        results = []
        for r in rows:
            results.append(
                {
                    "id": r[0],
                    "hs_code": r[1],
                    "description": r[2],
                    "chapter": r[3],
                    "policy": r[4],
                    "vector_score": float(r[5]),
                    "fts_score": float(r[6]),
                }
            )

        return results
