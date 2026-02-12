from hs.models import ItcHsMaster
from api.services.vector_service import VectorService
from api.services.llm_service import LLMService


class HSSearchService:

    def __init__(self):
        self.vector_service = VectorService()
        self.llm = LLMService()

    def like_search(self, query, schedule_type):
        return list(
            ItcHsMaster.objects.filter(
                description__icontains=query, schedule_type=schedule_type
            )[:20]
        )

    def embedding_search(self, query, schedule_type):

        # Embed query
        embedding = self.vector_service.embed(query)

        # Raw SQL for similarity ranking on HS master
        from django.db import connection

        with connection.cursor() as cur:
            cur.execute(
                """
                SELECT id, hs_code, description, policy,
                       embedding <=> %s::vector AS distance
                FROM itc_hs_master
                WHERE schedule_type = %s
                ORDER BY embedding <=> %s::vector
                LIMIT 20
                """,
                (embedding, schedule_type, embedding),
            )
            rows = cur.fetchall()

        return rows

    def merge_results(self, like_results, embed_rows):

        results = {}

        # Add LIKE results
        for r in like_results:
            results[r.hs_code] = r

        # Add embedding results
        for row in embed_rows:
            hs_code = row[1]
            if hs_code not in results:
                results[hs_code] = ItcHsMaster.objects.get(id=row[0])

        return list(results.values())[:20]

    def summarize(self, query, records):

        context = "\n".join([f"{r.hs_code} - {r.description}" for r in records[:10]])

        summary_prompt = f"""
Summarize the main classification trend for query:
{query}
"""

        return self.llm.get_reasoning(query=summary_prompt, context=context)

    def search(self, query, schedule_type, summarize=False):

        like_results = self.like_search(query, schedule_type)
        embed_rows = self.embedding_search(query, schedule_type)

        merged = self.merge_results(like_results, embed_rows)

        summary = None
        if summarize:
            summary = self.summarize(query, merged)

        return merged, summary
