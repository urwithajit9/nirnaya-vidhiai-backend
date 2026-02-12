import re
from hs.models import ItcHsMaster
from api.services.vector_service import VectorService
from api.services.llm_service import LLMService
from hs.services.prompt_service import build_qa_prompt


class HSAskService:

    HS_CODE_REGEX = r"\b\d{4,10}\b"

    def __init__(self):
        self.vector = VectorService()
        self.llm = LLMService()

    def extract_codes(self, text):
        return re.findall(self.HS_CODE_REGEX, text)

    def get_structured_context(self, codes, schedule_type):

        records = ItcHsMaster.objects.filter(
            hs_code__in=codes, schedule_type=schedule_type
        )

        context = ""

        for r in records:
            context += f"""
HS Code: {r.hs_code}
Description: {r.description}
Policy: {r.policy}
Policy Conditions: {r.policy_conditions}
Chapter: {r.chapter_num}
"""

        return context, list(records.values_list("hs_code", flat=True))

    def ask(self, question, schedule_type="import"):

        codes = self.extract_codes(question)

        structured_context, valid_codes = self.get_structured_context(
            codes, schedule_type
        )

        vector_docs = self.vector.find_context(query=question, limit=5)

        vector_context = "\n\n".join([d["content"] for d in vector_docs])

        full_context = f"""
STRUCTURED HS DATA:
{structured_context}

REGULATORY CONTEXT:
{vector_context}
"""

        answer = self.llm.get_reasoning(
            query=build_qa_prompt(question),
            context=full_context,
        )

        # 🔒 hallucination guard
        if not self.validate_hs_codes(answer, valid_codes):
            answer = "Unable to verify HS code consistency in generated response."

        return answer, vector_docs

    def validate_hs_codes(self, answer, valid_codes):

        found = re.findall(self.HS_CODE_REGEX, answer)

        for code in found:
            if code not in valid_codes:
                return False

        return True
