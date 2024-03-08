from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from django.contrib.auth.models import Group, User

import Personnel.models
import Personnel.forms as f

from . import models

# Register your models here.


admin.site.unregister(User)
admin.site.unregister(Group)


class PersonnelValuedSpecificationAdmin(TabularInline):
    model = models.PersonnelValuedSpecification
    extra = 0


@admin.register(models.Personnel)
class PersonnelAdmin(ModelAdmin):
    form = f.PersonnelForm
    list_display = [
        "first_name",
        "last_name",
        "role",
        "national_code",
        "display_status",
    ]
    fieldsets = [
        (
            "اطلاعات شخصی فرد",
            {
                "classes": ["collapse"],
                "fields": [
                    ("first_name", "last_name", "gender"),
                    "national_code",
                    "phone_number",
                    "birthdate",
                    "address",
                    "card_number",
                ],
            },
        ),
        (
            "اطلاعات پرسنلی",
            {
                "classes": ["collapse"],
                "fields": [
                    "role",
                    ("contract_date", "end_contract_date"),
                    ("status", "last_status_note"),
                    "note",
                ],
            },
        ),
        (
            "محدوده سرویس دهی",
            {
                "classes": ["collapse"],
                "description": "The service area can be many things",
                "fields": [
                    "areas",
                ],
            },
        ),
        (
            "ویژگی‌ها",
            {
                "classes": ["collapse"],
                "fields": [
                    "tag_specifications",
                ],
            },
        ),
    ]
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
