from hs.models import ItcHsMaster


class HSService:

    @staticmethod
    def get_by_code(hs_code: str, schedule_type: str):
        return ItcHsMaster.objects.filter(
            hs_code=hs_code, schedule_type=schedule_type
        ).first()

    @staticmethod
    def search_like(query: str, schedule_type: str):
        return ItcHsMaster.objects.filter(
            description__icontains=query, schedule_type=schedule_type
        )[:20]
