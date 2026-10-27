from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "age", "gender", "owner", "created_at")
    search_fields = ("name", "owner__email")
    list_filter = ("gender",)
