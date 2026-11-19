from django.contrib import admin

from core.models import (
    Candidate,
    Department,
    InterviewQuestionSet,
    JobPosition,
    Resume,
    ScreeningResult,
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name", "description")
    ordering = ("name",)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "created_at")
    search_fields = ("full_name", "email", "phone")
    list_filter = ("created_at",)
    date_hierarchy = "created_at"


@admin.register(JobPosition)
class JobPositionAdmin(admin.ModelAdmin):
    list_display = ("title", "department", "created_at")
    list_filter = ("department",)
    search_fields = ("title", "description", "department__name")
    list_select_related = ("department",)


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("candidate", "file", "uploaded_at")
    list_filter = ("uploaded_at",)
    search_fields = ("candidate__full_name", "candidate__email")
    list_select_related = ("candidate",)
    date_hierarchy = "uploaded_at"


@admin.register(ScreeningResult)
class ScreeningResultAdmin(admin.ModelAdmin):
    list_display = ("candidate", "job_position", "score", "recommendation", "generated_at")
    list_filter = ("recommendation", "job_position__department", "job_position", "generated_at")
    search_fields = ("candidate__full_name", "candidate__email", "job_position__title", "summary")
    list_select_related = ("candidate", "job_position", "job_position__department")
    date_hierarchy = "generated_at"


@admin.register(InterviewQuestionSet)
class InterviewQuestionSetAdmin(admin.ModelAdmin):
    list_display = ("candidate", "job_position", "screening_result", "generated_at")
    list_filter = ("job_position__department", "job_position", "generated_at")
    search_fields = ("candidate__full_name", "candidate__email", "job_position__title")
    list_select_related = ("candidate", "job_position", "screening_result")
    date_hierarchy = "generated_at"
