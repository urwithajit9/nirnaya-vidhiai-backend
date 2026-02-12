from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from hs.serializers import HSAskSerializer
from hs.services.ask_service import HSAskService


class HSAskView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = HSAskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question = serializer.validated_data["question"]

        service = HSAskService()
        answer, sources = service.ask(question)

        return Response({"answer": answer, "sources": sources})
