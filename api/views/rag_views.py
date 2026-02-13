from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import AskRequestSerializer
from api.services.vector_service import VectorService
from api.services.llm_service import LLMService


class AskView(APIView):
    def post(self, request):
        serializer = AskRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        query = serializer.validated_data["query"]
        top_k = serializer.validated_data["top_k"]

        vector_svc = VectorService()
        llm_svc = LLMService()

        sources = vector_svc.find_context(query, top_k)
        if not sources:
            return Response({
                "answer": "No relevant information found in the knowledge base.",
                "sources": []
            })
        context_str = "\n".join([s["content"] for s in sources])
        answer = llm_svc.get_reasoning(query, context_str)

        return Response({"answer": answer, "sources": sources})
