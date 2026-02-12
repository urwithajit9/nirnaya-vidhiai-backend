from hs.models import ItcHsMaster
from api.services.vector_service import VectorService


class HSRAGService:

    def __init__(self):
        self.vector_service = VectorService()

    def build_context_for_hs(self, hs_record: ItcHsMaster):

        structured_context = f"""
HS Code: {hs_record.hs_code}
Description: {hs_record.description}
Policy: {hs_record.policy}
Policy Conditions: {hs_record.policy_conditions}
Chapter: {hs_record.chapter_num}
        """

        vector_docs = self.vector_service.find_context(
            query=hs_record.description, limit=5
        )

        semantic_context = "\n\n".join([doc["content"] for doc in vector_docs])

        combined_context = f"""
STRUCTURED DATA:
{structured_context}

REGULATORY DOCUMENTS:
{semantic_context}
        """

        return combined_context, vector_docs
