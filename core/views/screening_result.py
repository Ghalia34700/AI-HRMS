from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import ScreeningResult
from core.serializers import ScreeningResultSerializer


@api_view(["GET"])
def screening_result_detail(request, pk):
    """GET /api/screening-results/<id>/ - 200 or 404."""
    screening_result = get_object_or_404(
        ScreeningResult.objects.select_related("candidate", "job_position"),
        pk=pk,
    )
    return Response(ScreeningResultSerializer(screening_result).data)