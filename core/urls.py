from django.urls import path

from core.views import (
    CandidateCreateView,
    DepartmentCreateView,
    JobPositionCreateView,
)

urlpatterns = [
    path("departments/", DepartmentCreateView.as_view(), name="department-create"),
    path("job-positions/", JobPositionCreateView.as_view(), name="job-position-create"),
    path("candidates/", CandidateCreateView.as_view(), name="candidate-create"),
]
