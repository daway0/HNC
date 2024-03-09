from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from . import models

# Register your models here.


class CallAdmin(admin.ModelAdmin):
    list_display = [
        "call_type",
        "status",
        "reason",
        "order_link",
        "contract_link",
    ]
    list_filter = [
        "call_type",
        "status",
        "reason",
    ]
    search_fields = [
        "order__client__first_name",
        "order__client__last_name",
        "contract__patients__first_name",
        "contract__patients__last_name",
    ]

    autocomplete_fields = ["reason", "order", "contract"]

    @admin.display(description="قرارداد مراقبت")
    def contract_link(self, obj):
        if not obj.contract:
            return
        app_label = obj.contract._meta.app_label
        model = obj.contract._meta.model_name
        url = reverse(
            "admin:%s_%s_change" % (app_label, model),
            args=[obj.contract.id],
        )
        return mark_safe(f"<a href='{url}'>{obj.contract}")

    @admin.display(description="خدمت موردی")
    def order_link(self, obj):
        if not obj.order:
            return
        
        app_label = obj.order._meta.app_label
        model = obj.order._meta.model_name
        url = reverse(
            "admin_%s_%s_change" % (app_label, model), args=[obj.order.id]
        )
        return mark_safe(f"<a href='{url}'>{obj.order}")


@admin.register(models.ClientCall)
class ClientCallAdmin(CallAdmin):
    list_display = [
        "id",
        "client",
        "raw_phone_number",
        "referral",
    ] + CallAdmin.list_display

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

    @admin.display(description="شماره تماس")
    def phone_number(self, obj):
        return obj.personnel.phone_number
