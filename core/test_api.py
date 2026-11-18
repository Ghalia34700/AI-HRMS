from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from core.models import Candidate, Department, JobPosition


class DepartmentCreateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("department-create")

    def test_creates_department(self):
        response = self.client.post(self.url, {"name": "Engineering", "description": "Builds things"}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "Engineering")
        self.assertTrue(Department.objects.filter(name="Engineering").exists())

    def test_name_is_required(self):
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.data)

    def test_duplicate_name_rejected(self):
        Department.objects.create(name="Engineering")
        response = self.client.post(self.url, {"name": "Engineering"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.data)
        self.assertEqual(Department.objects.count(), 1)

    def test_read_only_fields_ignored(self):
        response = self.client.post(self.url, {"id": 999, "name": "HR"}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.data["id"], 999)

    def test_get_not_allowed(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)


class JobPositionCreateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("job-position-create")
        self.department = Department.objects.create(name="Engineering")

    def test_creates_position_with_department_name(self):
        payload = {"department": self.department.id, "title": "Backend Developer", "required_skills": "Python, Django"}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["department"], self.department.id)
        self.assertEqual(response.data["department_name"], "Engineering")
        self.assertEqual(JobPosition.objects.count(), 1)

    def test_unknown_department_rejected(self):
        response = self.client.post(self.url, {"department": 9999, "title": "Ghost"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("department", response.data)
        self.assertEqual(JobPosition.objects.count(), 0)

    def test_department_and_title_required(self):
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("department", response.data)
        self.assertIn("title", response.data)

    def test_duplicate_title_in_same_department_rejected(self):
        JobPosition.objects.create(department=self.department, title="Backend Developer")
        response = self.client.post(
            self.url, {"department": self.department.id, "title": "Backend Developer"}, format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(JobPosition.objects.count(), 1)

    def test_same_title_in_other_department_allowed(self):
        other = Department.objects.create(name="Support")
        JobPosition.objects.create(department=self.department, title="Lead")
        response = self.client.post(self.url, {"department": other.id, "title": "Lead"}, format="json")
        self.assertEqual(response.status_code, 201)

    def test_get_not_allowed(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)


class CandidateCreateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("candidate-create")

    def test_registers_candidate(self):
        payload = {"full_name": "Sara Ali", "email": "sara@example.com", "phone": "0500000000"}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["email"], "sara@example.com")
        self.assertTrue(Candidate.objects.filter(email="sara@example.com").exists())

    def test_phone_is_optional(self):
        response = self.client.post(self.url, {"full_name": "Sara Ali", "email": "sara@example.com"}, format="json")
        self.assertEqual(response.status_code, 201)

    def test_required_fields(self):
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("full_name", response.data)
        self.assertIn("email", response.data)

    def test_invalid_email_rejected(self):
        response = self.client.post(self.url, {"full_name": "Sara", "email": "not-an-email"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.data)

    def test_duplicate_email_rejected(self):
        Candidate.objects.create(full_name="Sara Ali", email="sara@example.com")
        response = self.client.post(self.url, {"full_name": "Other", "email": "sara@example.com"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.data)
        self.assertEqual(Candidate.objects.count(), 1)

    def test_get_not_allowed(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)
