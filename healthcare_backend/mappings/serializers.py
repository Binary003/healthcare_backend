from rest_framework import serializers
from .models import PatientDoctorMapping
from patients.models import Patient
from doctors.models import Doctor

class MappingSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.name", read_only=True)
    doctor_name = serializers.CharField(source="doctor.name", read_only=True)
    doctor_specialization = serializers.CharField(source="doctor.specialization", read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = ("id", "patient", "patient_name", "doctor", "doctor_name", "doctor_specialization", "created_at")
        read_only_fields = ("id", "created_at", "patient_name", "doctor_name", "doctor_specialization")

    def validate_patient(self, patient):
        request = self.context["request"]
        if patient.owner_id != request.user.id:
            raise serializers.ValidationError("You can assign doctors only to your own patients.")
        return patient

    def validate(self, attrs):
        patient = attrs.get("patient", getattr(self.instance, "patient", None))
        doctor = attrs.get("doctor", getattr(self.instance, "doctor", None))
        if patient and doctor and PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exclude(pk=getattr(self.instance, "pk", None)).exists():
            raise serializers.ValidationError("This doctor is already assigned to this patient.")
        return attrs
