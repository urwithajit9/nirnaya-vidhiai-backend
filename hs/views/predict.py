from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from hs.services.predict_service import HSPredictService


class HSPredictView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        description = request.data.get("description")
        schedule_type = request.data.get("schedule_type")

        if not description or not schedule_type:
            return Response(
                {"error": "description and schedule_type required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if schedule_type not in ["import", "export"]:
            return Response(
                {"error": "schedule_type must be import/export"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        service = HSPredictService()
        result = service.predict(description, schedule_type)

        return Response(result)
