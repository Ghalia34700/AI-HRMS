from django.urls import path

from core.views import (
    CandidateCreateView,
    DepartmentCreateView,
    InterviewQuestionSetDetailView,
    JobPositionCreateView,
    ResumeUploadView,
    ScreeningResultDetailView,
)

urlpatterns = [
    path("departments/", DepartmentCreateView.as_view(), name="department-create"),
    path("job-positions/", JobPositionCreateView.as_view(), name="job-position-create"),
    path("candidates/", CandidateCreateView.as_view(), name="candidate-create"),
    path(
        "candidates/<int:candidate_id>/resumes/",
        ResumeUploadView.as_view(),
        name="resume-upload",
    ),
    path(
        "screening-results/<int:pk>/",
        ScreeningResultDetailView.as_view(),
        name="screening-result-detail",
    ),
    path(
        "interview-question-sets/<int:pk>/",
        InterviewQuestionSetDetailView.as_view(),
        name="interview-question-set-detail",
    ),
]
