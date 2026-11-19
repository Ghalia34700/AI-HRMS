from rest_framework import serializers
from core.models import Resume

ALLOWED_RESUME_EXTENSIONS = ("pdf", "docx", "txt")
MAX_RESUME_SIZE_BYTES = 5 * 1024 * 1024


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ["id", "candidate", "file", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]

    def validate_file(self, file):
        extension = (
            file.name.rsplit(".", 1)[-1].lower()
            if "." in file.name else ""
        )

        if extension not in ALLOWED_RESUME_EXTENSIONS:
            raise serializers.ValidationError(
                "Unsupported file type. Allowed types: PDF, DOCX, TXT."
            )

        if file.size > MAX_RESUME_SIZE_BYTES:
            raise serializers.ValidationError(
                "File is too large. The maximum size is 5 MB."
            )

        return file