from django.contrib import admin

# Register your models here.
from . import models


@admin.register(models.Patient, models.PatientValuedSpecification)
class PatientAdmin(admin.ModelAdmin):
    search_fields = ["first_name", "last_name", "national_code"]
