from rest_framework import serializers

from core.models import (
    Candidate,
    Department,
    InterviewQuestionSet,
    JobPosition,
    Resume,
    ScreeningResult,
)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name", "description", "created_at"]
        read_only_fields = ["id", "created_at"]


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ["id", "full_name", "email", "phone", "created_at"]
        read_only_fields = ["id", "created_at"]


class JobPositionSerializer(serializers.ModelSerializer):
    # `department` stays a writable id so clients can assign a department;
    # `department_name` is a read-only convenience so responses are readable.
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = JobPosition
        fields = [
            "id",
            "department",
            "department_name",
            "title",
            "description",
            "required_skills",
            "created_at"
        ]
        read_only_fields = ["id", "department_name", "created_at"]

    def validate_required_skills(self, value):
        if not isinstance(value, list) or not all(
                isinstance(s, str) and s.strip() for s in value
        ):
            raise serializers.ValidationError(
                "required_skills must be a list of non-empty strings."
            )
        return [s.strip() for s in value]


ALLOWED_RESUME_EXTENSIONS = ("pdf", "docx", "txt")
MAX_RESUME_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ["id", "candidate", "file", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]

    def validate_file(self, file):
        extension = file.name.rsplit(".", 1)[-1].lower() if "." in file.name else ""
        if extension not in ALLOWED_RESUME_EXTENSIONS:
            raise serializers.ValidationError(
                "Unsupported file type. Allowed types: PDF, DOCX, TXT."
            )
        if file.size > MAX_RESUME_SIZE_BYTES:
            raise serializers.ValidationError("File is too large. The maximum size is 5 MB.")
        return file


class ScreeningResultSerializer(serializers.ModelSerializer):
    """Read-only through the API: results are produced by the AI screening step."""

    candidate_name = serializers.CharField(source="candidate.full_name", read_only=True)
    job_position_title = serializers.CharField(source="job_position.title", read_only=True)

    class Meta:
        model = ScreeningResult
        fields = [
            "id",
            "candidate",
            "candidate_name",
            "job_position",
            "job_position_title",
            "score",
            "recommendation",
            "strengths",
            "missing_skills",
            "summary",
            "raw_report",
            "generated_at",
        ]
        read_only_fields = fields


class InterviewQuestionSetSerializer(serializers.ModelSerializer):
    """Read-only through the API: question sets are generated from a screening result."""

    candidate_name = serializers.CharField(source="candidate.full_name", read_only=True)
    job_position_title = serializers.CharField(source="job_position.title", read_only=True)

    class Meta:
        model = InterviewQuestionSet
        fields = [
            "id",
            "candidate",
            "candidate_name",
            "job_position",
            "job_position_title",
            "screening_result",
            "technical_questions",
            "behavioral_questions",
            "follow_up_questions",
            "generated_at",
        ]
        read_only_fields = fields
