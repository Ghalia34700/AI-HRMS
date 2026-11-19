from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers import JobPositionSerializer


class JobPositionCreateView(APIView):
    """POST /api/job-positions/ - create a job position under an existing department.

    Request body: {"department": <department id>, "title": "...", ...}

    201 with the created position (including `department_name`) on success.
    400 with per-field errors if the payload is invalid: a missing title, a
    department id that does not exist, or a title that already exists in that
    department.
    """

    def post(self, request):
        serializer = JobPositionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
