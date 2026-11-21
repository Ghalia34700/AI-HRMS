from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers import CandidateSerializer

@api_view(["POST"])
def candidate_create(request):
    """POST /api/candidates/ - 201 on success, 400 with per-field errors."""
    serializer = CandidateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)