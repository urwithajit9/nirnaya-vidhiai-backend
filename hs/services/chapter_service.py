from hs.models import ItcHsMaster
from api.services.llm_service import LLMService


class HSChapterService:

    def __init__(self):
        self.llm = LLMService()

    def get_chapter_codes(self, chapter_num, schedule_type):

        return ItcHsMaster.objects.filter(
            chapter_num=chapter_num, schedule_type=schedule_type, hs_level__in=[2, 4]
        ).order_by("hs_code")

    def generate_overview(self, chapter_num, records):

        context = "\n".join([f"{r.hs_code} - {r.description}" for r in records[:30]])

        prompt = f"""
Provide a high-level overview of Chapter {chapter_num}.
Explain major product categories and trade relevance.
"""

        return self.llm.get_reasoning(query=prompt, context=context)

    def get_chapter(self, chapter_num, schedule_type):

        records = self.get_chapter_codes(chapter_num, schedule_type)

        overview = self.generate_overview(chapter_num, records)

        return records, overview
