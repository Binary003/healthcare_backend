from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from patients.models import Patient
from doctors.models import Doctor
from .models import PatientDoctorMapping

User = get_user_model()

class MappingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="map@example.com", password="StrongPass!234", full_name="Mapper")
        self.other = User.objects.create_user(email="othermap@example.com", password="StrongPass!234", full_name="Other")
        self.patient = Patient.objects.create(owner=self.user, name="Patient", age=30, gender="male")
        self.doctor = Doctor.objects.create(created_by=self.other, name="Dr Public", specialization="General")

    def test_create_and_list_mapping(self):
        self.client.force_authenticate(self.user)
        response = self.client.post("/api/mappings/", {"patient": self.patient.id, "doctor": self.doctor.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        listing = self.client.get("/api/mappings/")
        self.assertEqual(len(listing.data), 1)

    def test_duplicate_assignment_is_rejected(self):
        PatientDoctorMapping.objects.create(patient=self.patient, doctor=self.doctor, assigned_by=self.user)
        self.client.force_authenticate(self.user)
        response = self.client.post("/api/mappings/", {"patient": self.patient.id, "doctor": self.doctor.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_map_someone_elses_patient(self):
        self.client.force_authenticate(self.other)
        response = self.client.post("/api/mappings/", {"patient": self.patient.id, "doctor": self.doctor.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
