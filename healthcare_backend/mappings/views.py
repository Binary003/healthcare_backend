from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from patients.models import Patient
from .models import PatientDoctorMapping
from .serializers import MappingSerializer

class MappingListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(patient__owner=self.request.user).select_related("patient", "doctor")

    def get(self, request):
        serializer = MappingSerializer(self.get_queryset(), many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = MappingSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        # The mapping can only refer to the current user's patient; serializer validates ownership.
        mapping = serializer.save(assigned_by=request.user)
        return Response(MappingSerializer(mapping, context={"request": request}).data, status=status.HTTP_201_CREATED)

class PatientMappingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        # Keep patient records private even when requesting mappings by ID.
        if not Patient.objects.filter(pk=patient_id, owner=request.user).exists():
            return Response({"detail": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)
        queryset = PatientDoctorMapping.objects.filter(patient_id=patient_id, patient__owner=request.user).select_related("patient", "doctor")
        return Response(MappingSerializer(queryset, many=True, context={"request": request}).data)

    def delete(self, request, patient_id):
        # DELETE path ID is the mapping ID per the assignment.
        try:
            mapping = PatientDoctorMapping.objects.select_related("patient").get(pk=patient_id, patient__owner=request.user)
        except PatientDoctorMapping.DoesNotExist:
            return Response({"detail": "Mapping not found."}, status=status.HTTP_404_NOT_FOUND)
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
