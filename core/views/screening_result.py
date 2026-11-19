from rest_framework import generics

from core.models import ScreeningResult
from core.serializers import ScreeningResultSerializer


class ScreeningResultDetailView(generics.RetrieveAPIView):
    """
    GET /api/screening-results/<id>/

    Retrieve one screening result.
    Returns 200 if found and 404 if not found.
    """

    queryset = ScreeningResult.objects.select_related(
        "candidate",
        "job_position"
    )
    serializer_class = ScreeningResultSerializer