from hs.models import ItcHsMaster
from django.db.models import Q
from django.db import connection
from typing import List, Dict


class HSRepository:

    def get_by_codes(self, codes: list[str]):
        return ItcHsMaster.objects.filter(hs_code__in=codes)

    def search_description(self, query: str, limit=20):
        return ItcHsMaster.objects.filter(description__icontains=query).order_by(
            "hs_code"
        )[:limit]

    def get_by_chapter(self, chapter_num: int):
        return ItcHsMaster.objects.filter(chapter_num=chapter_num).order_by("hs_code")

    def search_hybrid(
        self, query: str, embedding: List[float], schedule_type: str, limit=20
    ) -> List[Dict]:

        sql = """
        WITH fts AS (
            SELECT id, hs_code, description, policy, chapter_num,
                   ts_rank(to_tsvector('english', description),
                           plainto_tsquery('english', %s)) AS fts_rank
            FROM itc_hs_master
            WHERE schedule_type = %s
              AND to_tsvector('english', description)
                  @@ plainto_tsquery('english', %s)
            LIMIT %s
        ),
        vector AS (
            SELECT id, hs_code, description, policy, chapter_num,
                   1 - (embedding <=> %s::vector) AS similarity
            FROM knowledge_base
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        )
        SELECT * FROM fts;
        """

        params = [
            query,
            schedule_type,
            query,
            limit,
            embedding,
            embedding,
            limit,
        ]

        with connection.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()

        return rows
