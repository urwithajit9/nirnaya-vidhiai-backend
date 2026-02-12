from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from hs.serializers import HSSearchSerializer
from hs.services.search_service import HSSearchService


class HSSearchView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = HSSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        query = serializer.validated_data["query"]
        schedule_type = serializer.validated_data["schedule_type"]

        service = HSSearchService()
        results, summary = service.search(query, schedule_type, summarize=True)

        return Response(
            {
                "results": [
                    {
                        "hs_code": r.hs_code,
                        "description": r.description,
                        "policy": r.policy,
                    }
                    for r in results
                ],
                "ai_summary": summary,
            }
        )
