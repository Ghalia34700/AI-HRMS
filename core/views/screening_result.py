from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import ScreeningResult
from core.serializers import ScreeningResultSerializer


class ScreeningResultDetailView(APIView):
    """GET /api/screening-results/<id>/ - return one screening result.

    200 with the screening result on success.
    404 if no screening result has that id.
    """

    def get(self, request, pk):
        try:
            screening_result = ScreeningResult.objects.select_related(
                "candidate", "job_position"
            ).get(pk=pk)
        except ScreeningResult.DoesNotExist:
            return Response(
                {"detail": "Screening result not found."}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(ScreeningResultSerializer(screening_result).data)
