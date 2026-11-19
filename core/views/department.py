from rest_framework import generics

from core.models import Department
from core.serializers import DepartmentSerializer


class DepartmentCreateView(generics.CreateAPIView):
    """POST /api/departments/ - create a department.

    201 with the created department on success.
    400 with per-field errors if the payload is invalid (for example a missing
    or duplicate name).
    """

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer