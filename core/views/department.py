from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers import DepartmentSerializer

@api_view(["POST"])
def department_create(request):
    """POST /api/departments/ - 201 on success, 400 with per-field errors."""
    serializer = DepartmentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
