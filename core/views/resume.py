from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Candidate
from core.serializers import ResumeSerializer


class ResumeUploadView(APIView):
    """POST /api/candidates/<candidate_id>/resumes/ - upload a resume for a candidate.

    Send as multipart/form-data with the file in the `file` field.
    Only PDF, DOCX and TXT files up to 5 MB are accepted.

    201 with the created resume on success.
    404 if the candidate does not exist.
    400 with a `file` error if the file is missing, empty, too large or of an
    unsupported type.
    """

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, candidate_id):
        try:
            candidate = Candidate.objects.get(pk=candidate_id)
        except Candidate.DoesNotExist:
            return Response({"detail": "Candidate not found."}, status=status.HTTP_404_NOT_FOUND)

        # The candidate always comes from the URL, never from the request body.
        data = {"candidate": candidate.pk, "file": request.data.get("file")}
        serializer = ResumeSerializer(data=data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
