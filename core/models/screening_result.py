from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class ScreeningResult(models.Model):
    class Recommendation(models.TextChoices):
        PROCEED = "proceed", "Proceed"
        HOLD = "hold", "Hold"
        REJECT = "reject", "Reject"

    candidate = models.ForeignKey(
        "core.Candidate",
        on_delete=models.CASCADE,
        related_name="screening_results",
    )
    # PROTECT: keep screening history if someone tries to delete a position.
    job_position = models.ForeignKey(
        "core.JobPosition",
        on_delete=models.PROTECT,
        related_name="screening_results",
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    strengths = models.JSONField(default=list, blank=True)
    missing_skills = models.JSONField(default=list, blank=True)
    recommendation = models.CharField(max_length=10, choices=Recommendation.choices)
    summary = models.TextField(blank=True)
    # Full, unprocessed output of the AI screening step.
    raw_report = models.JSONField(default=dict, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "screening_result"
        ordering = ["-generated_at"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(score__gte=0, score__lte=100),
                name="screening_result_score_0_100",
            ),
        ]

    def __str__(self):
        return (
            f"{self.candidate.full_name} -> {self.job_position.title}: "
            f"{self.score} ({self.recommendation})"
        )