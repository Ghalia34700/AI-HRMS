from .candidate import CandidateCreateView
from .department import DepartmentCreateView
from .interview_question_set import InterviewQuestionSetDetailView
from .job_position import JobPositionCreateView
from .resume import ResumeUploadView
from .screening_result import ScreeningResultDetailView

__all__ = [
    "CandidateCreateView",
    "DepartmentCreateView",
    "InterviewQuestionSetDetailView",
    "JobPositionCreateView",
    "ResumeUploadView",
    "ScreeningResultDetailView",
]
