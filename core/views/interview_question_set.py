from rest_framework import generics
from core.models import InterviewQuestionSet
from core.serializers import InterviewQuestionSetSerializer


class InterviewQuestionSetDetailView(generics.CreateAPIView):
    """GET /api/interview-question-sets/<id>/ - return one interview question set.

    200 with the question set on success.
    404 if no question set has that id.
    """
    queryset = InterviewQuestionSet.objects.all()
    serializer_class = InterviewQuestionSetSerializer

