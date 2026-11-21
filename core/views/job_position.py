from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers import JobPositionSerializer


@api_view(["POST"])
def job_position_create(request):
    """POST /api/job-positions/ - 201 on success, 400 with per-field errors."""
    serializer = JobPositionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
