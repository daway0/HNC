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


class Client(Person):
    class Meta:
        verbose_name = "کارفرما"
        verbose_name_plural = "کارفرما ها"


class ClientPhoneNumber(m.Model):
    client = m.ForeignKey(Client, on_delete=m.CASCADE, verbose_name="کارفرما")

    class NumberTypeChoices(m.TextChoices):
        NORMAL = "N", "شماره تماس عادی"
        EMERGENCY = "E", "شماره تماس اضطراری"

    number_type = m.CharField(
        choices=NumberTypeChoices.choices,
        default=NumberTypeChoices.NORMAL,
        max_length=1,
        verbose_name="نوع شماره",
    )

    phone_number = m.CharField(max_length=11, verbose_name="شماره تلفن همراه")

    added_at = m.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "شماره تماس"
        verbose_name_plural = "شماره های تماس"

    def __str__(self):
        return f"{self.client.full_name} {self.phone_number}"


class ClientAddress(m.Model):
    client = m.ForeignKey(Client, on_delete=m.CASCADE)
    location_text = m.CharField(max_length=250, verbose_name="آدرس")

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس ها"

    def __str__(self):
        return f"{self.client.full_name} {self.location_text}"