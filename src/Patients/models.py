from BasicInfo.models import (
    CatalogValuedSpecification,
    Person,
)
from django.db import models as m


class Patient(Person):
    class Meta:
        verbose_name = "بیمار"
        verbose_name_plural = "بیمار ها"


class PatientValuedSpecification(m.Model):
    specification = m.ForeignKey(
        CatalogValuedSpecification,
        on_delete=m.SET_NULL,
        null=True,
    )
    patient = m.ForeignKey(Patient, on_delete=m.SET_NULL, null=True)
    value = m.CharField(max_length=250)

    class Meta:
        verbose_name = "ویژگی بیمار"
        verbose_name_plural = "ویژگی های بیمار"
