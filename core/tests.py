from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from core.models import (
    Candidate,
    Department,
    InterviewQuestionSet,
    JobPosition,
    Resume,
    ScreeningResult,
)
from core.serializers import (
    InterviewQuestionSetSerializer,
    JobPositionSerializer,
    ScreeningResultSerializer,
)

ALL_MODELS = [Candidate, Department, InterviewQuestionSet, JobPosition, Resume, ScreeningResult]


class SerializerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.department = Department.objects.create(name="Engineering")
        cls.position = JobPosition.objects.create(department=cls.department, title="Backend Developer")
        cls.candidate = Candidate.objects.create(full_name="Sara Ali", email="sara@example.com")
        cls.screening = ScreeningResult.objects.create(
            candidate=cls.candidate,
            job_position=cls.position,
            score=80,
            recommendation=ScreeningResult.Recommendation.PROCEED,
            missing_skills=["Docker"],
        )
        cls.questions = InterviewQuestionSet.objects.create(
            candidate=cls.candidate,
            job_position=cls.position,
            screening_result=cls.screening,
        )

    def test_job_position_shows_department_name(self):
        data = JobPositionSerializer(self.position).data
        self.assertEqual(data["department_name"], "Engineering")
        self.assertEqual(data["department"], self.department.id)

    def test_screening_result_is_read_only(self):
        serializer = ScreeningResultSerializer(self.screening)
        for name, field in serializer.fields.items():
            self.assertTrue(field.read_only, f"{name} should be read-only")

    def test_interview_question_set_is_read_only(self):
        serializer = InterviewQuestionSetSerializer(self.questions)
        for name, field in serializer.fields.items():
            self.assertTrue(field.read_only, f"{name} should be read-only")


class AdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = get_user_model().objects.create_superuser(
            username="admin", email="admin@example.com", password="pw"
        )

    def test_all_models_registered(self):
        for model in ALL_MODELS:
            self.assertTrue(admin.site.is_registered(model), model.__name__)

    def test_superuser_has_full_permissions_and_pages_load(self):
        self.client.force_login(self.superuser)
        for model in ALL_MODELS:
            ma = admin.site._registry[model]
            request = self.client.get("/").wsgi_request
            request.user = self.superuser
            self.assertTrue(ma.has_add_permission(request))
            self.assertTrue(ma.has_change_permission(request))
            self.assertTrue(ma.has_delete_permission(request))

            label = model._meta.model_name
            self.assertEqual(self.client.get(reverse(f"admin:core_{label}_changelist")).status_code, 200)
            self.assertEqual(self.client.get(reverse(f"admin:core_{label}_add")).status_code, 200)
