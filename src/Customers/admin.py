from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin

import common.utils as utils

from . import models


class ClientPhoneNumberAdmin(admin.TabularInline):
    model = models.ClientPhoneNumber
    extra = 0


class ClientAddressAdmin(admin.TabularInline):
    model = models.ClientAddress
    extra = 0


@admin.register(models.Patient, models.PatientValuedSpecification)
class PatientAdmin(admin.ModelAdmin):
    search_fields = ["first_name", "last_name", "national_code"]


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    search_fields = ["first_name", "last_name"]
    inlines = [ClientPhoneNumberAdmin, ClientAddressAdmin]
    list_display = ["first_name", "last_name", "phone_number", "address"]

    @admin.display(description="تلفن همراه")
    def phone_number(self, obj):
        return (
            models.ClientPhoneNumber.objects.filter(client=obj)
            .last()
            .phone_number
        )

    @admin.display(description="آدرس")
    def address(self, obj):
        return utils.beautify_string_cut(
            models.ClientAddress.objects.filter(client=obj)
            .last()
            .location_text
        )
