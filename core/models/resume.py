from django.db import models
from pip._internal.resolution.resolvelib.base import Candidate


class Resume(models.Model):
    candidate = models.ForeignKey(
        "core.Candidate",
        on_delete=models.CASCADE,
        related_name="resumes",
    )
    file = models.FileField(upload_to="resumes/%Y/%m %H:%M")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "resume"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.candidate.full_name} - {self.uploaded_at:%Y-%m-%d %H:%M}"