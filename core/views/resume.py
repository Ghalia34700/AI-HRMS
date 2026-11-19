from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Candidate
from core.serializers import ResumeSerializer


class ResumeUploadView(APIView):
    """
    POST /api/candidates/<candidate_id>/resumes/

    Upload a resume for an existing candidate.

    Accepted formats: PDF, DOCX, TXT.
    Maximum file size: 5 MB.
    """

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, candidate_id):
        # Find the candidate
        try:
            candidate = Candidate.objects.get(pk=candidate_id)
        except Candidate.DoesNotExist:
            return Response(
                {"detail": "Candidate not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get the uploaded file
        data = {
            "candidate": candidate.pk,
            "file": request.data.get("file")
        }

        # Validate the resume
        serializer = ResumeSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Save the resume
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )