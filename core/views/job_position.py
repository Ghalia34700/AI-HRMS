from rest_framework.response import Response
from rest_framework import generics
from core.serializers import JobPositionSerializer
from core.models import JobPosition


class JobPositionCreateView(generics.CreateAPIView):
    """POST /api/job-positions/ - create a job position under an existing department.

    Request body: {"department": <department id>, "title": "...", ...}

    201 with the created position (including `department_name`) on success.
    400 with per-field errors if the payload is invalid: a missing title, a
    department id that does not exist, or a title that already exists in that
    department.
    """

    queryset = JobPosition.objects.all()
    serializer_class = JobPositionSerializer