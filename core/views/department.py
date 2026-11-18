from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers import DepartmentSerializer


class DepartmentCreateView(APIView):
    """POST /api/departments/ - create a department.

    201 with the created department on success.
    400 with per-field errors if the payload is invalid (for example a missing
    or duplicate name).
    """

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
