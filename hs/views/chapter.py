from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from hs.services.chapter_service import HSChapterService


class HSChapterView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, chapter_num):

        schedule_type = request.query_params.get("schedule_type", "import")

        service = HSChapterService()

        records, overview = service.get_chapter(chapter_num, schedule_type)

        return Response(
            {
                "chapter": chapter_num,
                "overview": overview,
                "codes": [
                    {
                        "hs_code": r.hs_code,
                        "description": r.description,
                        "policy": r.policy,
                    }
                    for r in records
                ],
            }
        )
