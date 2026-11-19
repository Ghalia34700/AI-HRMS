from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import InterviewQuestionSet
from core.serializers import InterviewQuestionSetSerializer


class InterviewQuestionSetDetailView(APIView):
    """GET /api/interview-question-sets/<id>/ - return one interview question set.

    200 with the question set on success.
    404 if no question set has that id.
    """

    def get(self, request, pk):
        try:
            question_set = InterviewQuestionSet.objects.select_related(
                "candidate", "job_position"
            ).get(pk=pk)
        except InterviewQuestionSet.DoesNotExist:
            return Response(
                {"detail": "Interview question set not found."}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(InterviewQuestionSetSerializer(question_set).data)
