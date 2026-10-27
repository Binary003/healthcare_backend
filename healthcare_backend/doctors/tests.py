from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Doctor

User = get_user_model()

class DoctorPermissionsTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(email="docowner@example.com", password="StrongPass!234", full_name="Owner")
        self.other = User.objects.create_user(email="docother@example.com", password="StrongPass!234", full_name="Other")
        self.doctor = Doctor.objects.create(created_by=self.owner, name="Dr A", specialization="Cardiology")

    def test_directory_is_visible_to_authenticated_users(self):
        self.client.force_authenticate(self.other)
        response = self.client.get("/api/doctors/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_only_creator_can_update_doctor(self):
        self.client.force_authenticate(self.other)
        response = self.client.patch(f"/api/doctors/{self.doctor.id}/", {"name": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
