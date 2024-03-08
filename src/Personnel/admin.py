from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from django.contrib.auth.models import Group, User
from jalali_date.admin import ModelAdminJalaliMixin

import Personnel.models

# Register your models here.
from . import forms, models


class PersonnelValuedSpecificationAdmin(TabularInline):
    model = models.PersonnelValuedSpecification
    extra = 0


@admin.register(models.Personnel)
class PersonnelAdmin(ModelAdmin):
    form = forms.PersonnelForm
    list_display = [
        "first_name",
        "last_name",
        "role",
        "national_code",
        "display_status",
    ]
    # fieldsets = [
    #     (
    #         "User Basic Information",
    #         {
    #             "fields": [
    #                 ("first_name", "last_name", "gender"),
    #                 "national_code",
    #                 "phone_number",
    #                 "birthdate",
    #                 "address",
    #                 "card_number"
    #                 ],
    #             },
    #         ),
    #     (
    #         "Personnel Information",
    #         {
    #             "fields": [
    #                 "role",
    #                 ("contract_date", "end_contract_date"),
    #                 ("status", "last_status_note"),
    #                 "note"],
    #             },
    #         ),
    #     (
    #         "Service Area",
    #         {
    #
    #             "classes": ["collapse"],
    #             "description": "The service area can be many things",
    #             "fields": [
    #                 "areas",
    #                 ],
    #             },
    #         ),
    #     (
    #         "Specification",
    #         {
    #
    #             "classes": ["collapse"],
    #             "fields": [
    #                 "tag_specifications",
    #                 ],
    #             },
    #         ),
    #     ]
    filter_horizontal = ["areas", "tag_specifications"]
    list_filter = ["status"]
    search_fields = ["first_name", "last_name"]
    inlines = [PersonnelValuedSpecificationAdmin]

    @admin.display(description="test")
    def test(self): ...

    @admin.display(
        description="Status",
    )
    def display_status(self, instance):
        if instance.status:
            return instance.get_status_display()

        return None
