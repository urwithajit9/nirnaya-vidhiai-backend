import re
from api.services.vector_service import VectorService
from api.services.llm_service import LLMService
from hs.services.predict_repository import HSPredictRepository
from hs.services.prompt_service import build_predict_prompt


class HSPredictService:

    HS_CODE_REGEX = r"\b\d{4,10}\b"

    def __init__(self):
        self.vector = VectorService()
        self.repo = HSPredictRepository()
        self.llm = LLMService()

    def predict(self, description: str, schedule_type: str):

        embedding = self.vector.embed(description)

        candidates = self.repo.hybrid_search(
            query=description,
            embedding=embedding,
            schedule_type=schedule_type,
            limit=10,
        )

        if not candidates:
            return {"error": "No matching HS codes found."}

        # Weighted score
        for c in candidates:
            c["final_score"] = 0.7 * c["vector_score"] + 0.3 * c["fts_score"]

        candidates.sort(key=lambda x: x["final_score"], reverse=True)

        top_candidates = candidates[:5]

        # LLM reasoning (restricted)
        explanation = self.llm.get_reasoning(
            query=build_predict_prompt(description, top_candidates), context=""
        )

        selected_code = self.extract_code(explanation)

        # Validate selection
        valid_codes = [c["hs_code"] for c in top_candidates]

        if selected_code not in valid_codes:
            # deterministic fallback
            selected_code = top_candidates[0]["hs_code"]

        selected = next(c for c in top_candidates if c["hs_code"] == selected_code)

        return {
            "predicted_hs_code": selected["hs_code"],
            "description": selected["description"],
            "chapter": selected["chapter"],
            "confidence": round(selected["final_score"], 3),
            "top_matches": top_candidates,
            "explanation": explanation,
        }

    def extract_code(self, text):
        match = re.search(self.HS_CODE_REGEX, text)
        return match.group() if match else None
