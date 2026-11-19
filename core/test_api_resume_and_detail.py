import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from core.models import (
    Candidate,
    Department,
    InterviewQuestionSet,
    JobPosition,
    Resume,
    ScreeningResult,
)
from core.serializers import MAX_RESUME_SIZE_BYTES

TEMP_MEDIA = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class ResumeUploadTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA, ignore_errors=True)

    def setUp(self):
        self.client = APIClient()
        self.candidate = Candidate.objects.create(full_name="Sara Ali", email="sara@example.com")
        self.url = reverse("resume-upload", args=[self.candidate.id])

    def upload(self, name, content=b"data", url=None, **extra):
        return self.client.post(
            url or self.url,
            {"file": SimpleUploadedFile(name, content), **extra},
            format="multipart",
        )

    def test_accepts_allowed_types(self):
        for name in ("cv.pdf", "cv.docx", "cv.txt", "CV.PDF"):
            with self.subTest(name=name):
                response = self.upload(name)
                self.assertEqual(response.status_code, 201, response.data)
                self.assertEqual(response.data["candidate"], self.candidate.id)
                self.assertIn("file", response.data)
        self.assertEqual(Resume.objects.filter(candidate=self.candidate).count(), 4)

    def test_rejects_unsupported_types(self):
        for name in ("cv.exe", "cv.doc", "cv.png", "cv", "cv.pdf.exe"):
            with self.subTest(name=name):
                response = self.upload(name)
                self.assertEqual(response.status_code, 400)
                self.assertIn("file", response.data)
        self.assertEqual(Resume.objects.count(), 0)

    def test_missing_file(self):
        response = self.client.post(self.url, {}, format="multipart")
        self.assertEqual(response.status_code, 400)
        self.assertIn("file", response.data)

    def test_file_sent_as_plain_text_rejected(self):
        response = self.client.post(self.url, {"file": "cv.pdf"}, format="multipart")
        self.assertEqual(response.status_code, 400)
        self.assertIn("file", response.data)

    def test_empty_file_rejected(self):
        response = self.upload("cv.pdf", b"")
        self.assertEqual(response.status_code, 400)
        self.assertIn("file", response.data)

    def test_too_large_file_rejected(self):
        response = self.upload("cv.pdf", b"x" * (MAX_RESUME_SIZE_BYTES + 1))
        self.assertEqual(response.status_code, 400)
        self.assertIn("file", response.data)

    def test_unknown_candidate_returns_404(self):
        response = self.upload("cv.pdf", url=reverse("resume-upload", args=[9999]))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["detail"], "Candidate not found.")

    def test_huge_candidate_id_returns_404_not_500(self):
        response = self.upload("cv.pdf", url=reverse("resume-upload", args=[10**30]))
        self.assertEqual(response.status_code, 404)

    def test_candidate_in_body_is_ignored(self):
        other = Candidate.objects.create(full_name="Other", email="other@example.com")
        response = self.upload("cv.pdf", candidate=other.id)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["candidate"], self.candidate.id)

    def test_json_body_gets_clear_error(self):
        response = self.client.post(self.url, {"file": "x"}, format="json")
        self.assertEqual(response.status_code, 415)
        self.assertIn("detail", response.data)

    def test_get_not_allowed(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)


class DetailEndpointTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        department = Department.objects.create(name="Engineering")
        cls.position = JobPosition.objects.create(department=department, title="Backend Developer")
        cls.candidate = Candidate.objects.create(full_name="Sara Ali", email="sara@example.com")
        cls.screening = ScreeningResult.objects.create(
            candidate=cls.candidate,
            job_position=cls.position,
            score=80,
            recommendation=ScreeningResult.Recommendation.PROCEED,
            missing_skills=ScreeningResult.Recommendation.HOLD,
            strengths=["Python"],
            summary="Strong fit",
        )
        cls.questions = InterviewQuestionSet.objects.create(
            candidate=cls.candidate,
            job_position=cls.position,
            screening_result=cls.screening,
            technical_questions=["Explain the GIL"],
            behavioural_questions=["Tell me about a conflict"],
            follow_up_questions=["Why Django?"],
        )

    def setUp(self):
        self.client = APIClient()

    def test_screening_result_found(self):
        response = self.client.get(reverse("screening-result-detail", args=[self.screening.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.screening.id)
        self.assertEqual(response.data["score"], 80)
        self.assertEqual(response.data["candidate_name"], "Sara Ali")
        self.assertEqual(response.data["job_position_title"], "Backend Developer")
        self.assertEqual(response.data["strengths"], ["Python"])

    def test_screening_result_not_found(self):
        response = self.client.get(reverse("screening-result-detail", args=[9999]))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["detail"], "Screening result not found.")

    def test_screening_result_huge_id_is_404_not_500(self):
        response = self.client.get(reverse("screening-result-detail", args=[10**30]))
        self.assertEqual(response.status_code, 404)

    def test_screening_result_is_get_only(self):
        url = reverse("screening-result-detail", args=[self.screening.id])
        for method in ("post", "put", "patch", "delete"):
            with self.subTest(method=method):
                self.assertEqual(getattr(self.client, method)(url).status_code, 405)

    def test_question_set_found(self):
        response = self.client.get(reverse("interview-question-set-detail", args=[self.questions.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.questions.id)
        self.assertEqual(response.data["screening_result"], self.screening.id)
        self.assertEqual(response.data["technical_questions"], ["Explain the GIL"])
        self.assertEqual(response.data["behavioural_questions"], ["Tell me about a conflict"])
        self.assertEqual(response.data["follow_up_questions"], ["Why Django?"])

    def test_question_set_not_found(self):
        response = self.client.get(reverse("interview-question-set-detail", args=[9999]))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["detail"], "Interview question set not found.")

    def test_question_set_huge_id_is_404_not_500(self):
        response = self.client.get(reverse("interview-question-set-detail", args=[10**30]))
        self.assertEqual(response.status_code, 404)

    def test_question_set_is_get_only(self):
        url = reverse("interview-question-set-detail", args=[self.questions.id])
        for method in ("post", "put", "patch", "delete"):
            with self.subTest(method=method):
                self.assertEqual(getattr(self.client, method)(url).status_code, 405)
