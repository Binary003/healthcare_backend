from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ("id", "name", "age", "gender", "phone", "address", "medical_history", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_age(self, value):
        if not 0 <= value <= 125:
            raise serializers.ValidationError("Age must be between 0 and 125.")
        return value
