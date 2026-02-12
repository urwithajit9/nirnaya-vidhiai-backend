from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from hs.serializers import HSAnalyzeSerializer
from hs.services.hs_service import HSService
from hs.services.rag_service import HSRAGService
from hs.services.prompt_service import build_analysis_prompt
from api.services.llm_service import LLMService


class HSAnalyzeView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = HSAnalyzeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        hs_code = serializer.validated_data["hs_code"]
        schedule_type = serializer.validated_data["schedule_type"]

        hs_record = HSService.get_by_code(hs_code, schedule_type)

        if not hs_record:
            return Response({"error": "Invalid HS Code"}, status=404)

        rag_service = HSRAGService()
        context, sources = rag_service.build_context_for_hs(hs_record)

        llm = LLMService()
        explanation = llm.get_reasoning(query=build_analysis_prompt(), context=context)

        return Response(
            {
                "hs_code": hs_record.hs_code,
                "description": hs_record.description,
                "policy": hs_record.policy,
                "policy_conditions": hs_record.policy_conditions,
                "ai_explanation": explanation,
                "sources": sources,
            }
        )
