from django.db import models


class InterviewQuestionSet(models.Model):
    candidate = models.ForeignKey(
        "core.Candidate",
        on_delete=models.CASCADE,
        related_name="interview_question_sets",
    )
    job_position = models.ForeignKey(
        "core.JobPosition",
        on_delete=models.PROTECT,
        related_name="interview_question_sets",
    )
    # CASCADE: the questions are derived from the screening result.
    screening_result = models.ForeignKey(
        "core.ScreeningResult",
        on_delete=models.CASCADE,
        related_name="interview_question_sets",
    )
    technical_questions = models.JSONField(default=list, blank=True)
    behavioral_questions = models.JSONField(default=list, blank=True)
    follow_up_questions = models.JSONField(default=list, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "interview_question_set"
        ordering = ["-generated_at"]

    def __str__(self):
        return f"Questions for {self.candidate.full_name} - {self.job_position.title}"