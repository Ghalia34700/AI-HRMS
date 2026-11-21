from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from core.models import Candidate
from core.serializers import ResumeSerializer


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def resume_upload(request, candidate_id):
    """POST /api/candidates/<candidate_id>/resumes/ - 201, 404 or 400."""
    candidate = get_object_or_404(Candidate, pk=candidate_id)

    # The candidate always comes from the URL, never from the request body.
    data = {"candidate": candidate.pk, "file": request.data.get("file")}
    serializer = ResumeSerializer(data=data, context={"request": request})
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)