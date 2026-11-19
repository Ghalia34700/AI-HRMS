from rest_framework import serializers
from core.models import JobPosition


class JobPositionSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(
        source="department.name",
        read_only=True
    )

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