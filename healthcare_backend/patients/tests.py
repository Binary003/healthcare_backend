from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Patient

User = get_user_model()

class PatientAccessTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(email="owner@example.com", password="StrongPass!234", full_name="Owner")
        self.other = User.objects.create_user(email="other@example.com", password="StrongPass!234", full_name="Other")
        self.patient = Patient.objects.create(owner=self.owner, name="Patient One", age=28, gender="other")

    def test_users_only_see_their_patients(self):
        self.client.force_authenticate(self.other)
        response = self.client.get("/api/patients/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_cannot_read_another_users_patient(self):
        self.client.force_authenticate(self.other)
        response = self.client.get(f"/api/patients/{self.patient.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
