from rest_framework import serializers
from .models import Doctor

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ("id", "name", "specialization", "email", "phone", "experience_years", "clinic_address", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_experience_years(self, value):
        if value > 80:
            raise serializers.ValidationError("Experience years must be 80 or less.")
        return value
