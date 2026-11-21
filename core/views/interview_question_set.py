from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from core.models import InterviewQuestionSet
from core.serializers import InterviewQuestionSetSerializer

@api_view(["GET"])
def interview_question_set_detail(request, pk):
    """GET /api/interview-question-sets/<id>/ - 200 or 404."""
    question_set = get_object_or_404(
        InterviewQuestionSet.objects.select_related("candidate", "job_position"),
        pk=pk,
    )
    return Response(InterviewQuestionSetSerializer(question_set).data)