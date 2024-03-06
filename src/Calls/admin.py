from django.contrib import admin

from . import models

# Register your models here.


class CallAdmin(admin.ModelAdmin):
    list_display = [
        "call_type",
        "status",
        "reason",
        "order",
        "contract",
    ]
    list_filter = [
        "call_type",
        "status",
        "reason",
    ]
    list_display_links = [
        "order",
        "contract",
    ]
    search_fields = [
        "order__client__first_name",
        "order__client__last_name",
        "contract__patients__first_name",
        "contract__patients__last_name",
    ]

    autocomplete_fields = ["reason", "order", "contract"]


@admin.register(models.ClientCall)
class ClientCallAdmin(CallAdmin):
    list_display = [
        "id",
        "client",
        "raw_phone_number",
        "referral",
    ] + CallAdmin.list_display

    list_display_links = ["id"] + CallAdmin.list_display_links

    search_fields = [
        "client__first_name",
        "client__last_name",
        "raw_phone_number",
    ] + CallAdmin.search_fields

    autocomplete_fields = ["client"] + CallAdmin.autocomplete_fields


@admin.register(models.PersonnelCall)
class PersonnelCallAdmin(CallAdmin):
    list_display = [
        "personnel",
        "phone_number",
    ] + CallAdmin.list_display

    search_fields = [
        "personnel__first_name",
        "personnel__last_name",
    ] + CallAdmin.search_fields

    list_display_links = ["personnel"] + CallAdmin.list_display_links

    @admin.display(description="شماره تماس")
    def phone_number(self, obj):
        return obj.personnel.phone_number
