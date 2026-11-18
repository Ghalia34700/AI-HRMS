from django.db import models

class JobPosition(models.Model):
    # PROTECT: a department with open positions cannot be deleted by accident.
    department = models.ForeignKey(
        'core.Department',
        on_delete=models.PROTECT,
        related_name='job_positions',
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    required_skills = models.TextField(blank=True)

    class Meta:
        db_table = "job_position"
        ordering = ["department__name", "title"]
        constraints = [
            models.UniqueConstraint(
                fields=["department", "title"],
                name="uniq_job_position_title_per_department",
            ),
        ]

    def __str__(self):
        return f"{self.title} ({self.department.name})"