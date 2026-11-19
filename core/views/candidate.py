
from rest_framework import generics
from core.models import Candidate
from core.serializers import CandidateSerializer


class CandidateCreateView(generics.CreateAPIView):
    """POST /api/candidates/ - register a candidate.

    201 with the created candidate on success.
    400 with per-field errors if the payload is invalid (for example a missing
    name, a malformed email or an email that is already registered).
    """

    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer