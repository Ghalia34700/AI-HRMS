from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers import CandidateSerializer


class CandidateCreateView(APIView):
    """POST /api/candidates/ - register a candidate.

    201 with the created candidate on success.
    400 with per-field errors if the payload is invalid (for example a missing
    name, a malformed email or an email that is already registered).
    """

    def post(self, request):
        serializer = CandidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
