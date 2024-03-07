from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin, TabularInline
from django.contrib.admin.options import BaseModelAdmin
from django.contrib.admin.widgets import AdminTextInputWidget
from django.db import models as django_main_models
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.safestring import mark_safe

import Orders.forms
import utils
from BasicInfo.admin import CatalogAdmin
from Calls.models import ClientCall, PersonnelCall
from Financial.models import IncomingPayment, OutgoingPayment

from . import farsi_messages as fm
from . import models


class TextInputIntegerFieldModelAdminMixin(BaseModelAdmin):
    formfield_overrides = {
        django_main_models.IntegerField: {"widget": AdminTextInputWidget}
    }


class ClientPhoneNumberAdmin(TabularInline):
    model = models.ClientPhoneNumber
    extra = 0


class ClientAddressAdmin(TabularInline):
    model = models.ClientAddress
    extra = 0


class ReadOnlyTabular(TabularInline):
    classes = ["collapse"]

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class PersonnelCallInline(ReadOnlyTabular):
    model = PersonnelCall


class ClientCallInline(ReadOnlyTabular):
    model = ClientCall


class IncomingPaymentInline(ReadOnlyTabular):
    model = IncomingPayment


class OutgoingPaymentInline(ReadOnlyTabular):
    model = OutgoingPayment


class CommentAdmin(TabularInline):
    extra = 0
    classes = ["collapse"]
    readonly_fields = ["created_at"]

    def has_change_permission(self, request, obj=None):
        return False


class OrderCommentAdmin(CommentAdmin):
    model = models.OrderComment


class ContractCommentAdmin(CommentAdmin):
    model = models.ContractComment


@admin.register(models.CareContract)
class CareContractAdmin(ModelAdmin, TextInputIntegerFieldModelAdminMixin):
    form = Orders.forms.CareContractForm
    list_display = [
        "client_full_name",
        "personnel",
        "shift",
        "personnel_monthly_salary",
        "healthcare_franchise_amount",
        "client_payment_status",
        "personnel_payment_status",
        "include_holidays",
    ]
    filter_horizontal = ["shift_days", "patients"]
    list_editable = ["healthcare_franchise_amount", "personnel_monthly_salary"]
    list_filter = [
        "client_payment_status",
        "personnel_payment_status",
    ]
    autocomplete_fields = [
        "client",
        "referral_personnel",
        "referral_client",
        "referral_other_healthcare",
        "personnel",
    ]
    search_fields = ["PersonnelCall", "ClientCall"]
    inlines = [
        IncomingPaymentInline,
        PersonnelCallInline,
        ClientCallInline,
        ContractCommentAdmin,
    ]

    fieldsets = [
        (
            "کارفرما و بیمار‌ ها",
            {
                "classes": ["collapse"],
                "fields": [
                    "care_for",
                    "patients",
                    "client",
                    "relationship_with_patient",
                    "relationship_with_patient_note",
                ],
            },
        ),
        (
            "معرف",
            {
                "classes": ["collapse"],
                "fields": [
                    "referral",
                    "referral_personnel",
                    "referral_client",
                    "referral_other_healthcare",
                ],
            },
        ),
        (
            "مراقب",
            {
                "classes": ["collapse"],
                "fields": [
                    "personnel",
                    "shift",
                    "shift_days",
                    "shift_start",
                    "shift_end",
                ],
            },
        ),
        (
            "محل خدمت و بازه زمانی",
            {
                "classes": ["collapse"],
                "fields": [
                    "service_location",
                    "start",
                    "end",
                    "include_holidays",
                ],
            },
        ),
        (
            "اطلاعات مالی",
            {
                "classes": ["collapse"],
                "fields": [
                    "personnel_monthly_salary",
                    "personnel_salary_payment_time",
                    "personnel_payment_status",
                    "client_payment_status",
                    "healthcare_franchise_amount",
                ],
            },
        ),
    ]

    @admin.display(description="کارفرما")
    def client_full_name(self, obj):
        return "%s %s" % (obj.client.first_name, obj.client.last_name)


@admin.register(models.Client)
class ClientAdmin(ModelAdmin):
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


class OrderServiceAdmin(TabularInline, TextInputIntegerFieldModelAdminMixin):
    model = models.OrderService
    extra = 0
    autocomplete_fields = ["service"]
    classes = ["collapse"]


@admin.register(models.Order)
class OrderAdmin(ModelAdmin, TextInputIntegerFieldModelAdminMixin):
    list_display = [
        "display_service_card",
        "assigned_personnel",
        "order_status",
        "display_total_order_cost",
        "display_discount_cost",
        "display_custom_actions",
    ]

    autocomplete_fields = [
        "client",
        "assigned_personnel",
        "referral_personnel",
        "referral_client",
        "referral_other_healthcare",
    ]

    fieldsets = [
        (
            "اطلاعات پایه",
            {
                "classes": ["collapse"],
                "fields": [
                    ("client", "assigned_personnel"),
                    ("order_status", "service_location"),
                    (
                        "client_payment_status",
                        "personnel_payment_status",
                    ),
                ],
            },
        ),
        (
            "معرف",
            {
                "classes": ["collapse"],
                "fields": [
                    "referral",
                    (
                        "referral_personnel",
                        "referral_client",
                        "referral_other_healthcare",
                    ),
                ],
            },
        ),
        (
            "تاریخ و زمان های مرتبط",
            {
                "classes": ["collapse"],
                "fields": [
                    ("requested", "accepted", "done"),
                ],
            },
        ),
        (
            "خصوصیات بیمار",
            {
                "classes": ["collapse"],
                "fields": ["patient_tag_specifications"],
            },
        ),
        (
            "تخفیف",
            {
                "classes": ["collapse"],
                "fields": ["discount"],
            },
        ),
    ]

    filter_horizontal = ["areas", "tag_specifications"]
    # list_filter = ["status"]
    inlines = [
        OrderServiceAdmin,
        # OrderEquipmentAdmin
        OrderCommentAdmin,
        ClientCallInline,
        PersonnelCallInline,
        IncomingPaymentInline,
        OutgoingPaymentInline,
    ]
    filter_horizontal = ["patient_tag_specifications"]

    search_fields = [CatalogAdmin]
    readonly_fields = [
        "client_payment_status",
        "personnel_payment_status",
        "requested",
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "<path:object_id>/client-payment/",
                self.admin_site.admin_view(self.new_client_payment),
                name="order_client_payment",
            ),
            path(
                "<path:object_id>/client-payment/<int" ":payment_id>/remove/",
                self.admin_site.admin_view(self.remove_client_payment_record),
                name="order_client_payment_remove",
            ),
            path(
                "<path:object_id>/personnel-payment/",
                self.admin_site.admin_view(self.new_personnel_payment),
                name="order_personnel_payment",
            ),
            path(
                "<path:object_id>/personnel-payment/<int"
                ":payment_id>/remove/",
                self.admin_site.admin_view(
                    self.remove_personnel_payment_record
                ),
                name="order_personnel_payment_remove",
            ),
        ]
        return my_urls + urls

    def remove_client_payment_record(self, request, object_id, payment_id):
        order = Orders.models.Order.objects.get(id=object_id)
        payment_record = Financial.models.IncomingPayment.objects.filter(
            id=payment_id
        )
        if payment_record:
            payment_record.delete()
            order.refresh_order_payment_statuses()
            messages.add_message(
                request,
                messages.SUCCESS,
                message=fm.order_remove_client_payment_record_success,
            )
        else:
            messages.add_message(
                request,
                messages.WARNING,
                message=fm.order_remove_client_payment_record_record_not_found,
            )
        return redirect(
            reverse("admin:order_client_payment", args=(object_id,))
        )

    def new_client_payment(self, request, object_id):
        order = Orders.models.Order.objects.get(id=object_id)
        if request.method == "POST":
            form = Orders.forms.OrderClientPaymentForm(request.POST)
            if form.is_valid():
                data = utils.map_to_model_data(
                    form.cleaned_data,
                    [
                        ("paid_at",),
                        ("new_payment_amount", "paid_amount"),
                        ("description", "payment_desc"),
                    ],
                )
                data["from_user"] = order.client
                data["order"] = order

                try:
                    Financial.models.IncomingPayment.objects.create(**data)
                    order.refresh_order_payment_statuses()
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        message=fm.order_success_client_payment,
                    )
                except Exception as e:
                    messages.add_message(
                        request, messages.ERROR, message=e.__str__()
                    )
                finally:
                    return redirect(
                        reverse(
                            "admin:order_client_payment", args=(object_id,)
                        )
                    )

        form = Orders.forms.OrderClientPaymentForm(
            initial=dict(
                remaining_amount=order.client_remaining_payable,
                new_payment_amount=order.client_remaining_payable,
                paid_at=utils.current_date_str(),
            )
        )
        context = dict(
            self.admin_site.each_context(request),
            form=form,
            order=order,
            payment_records=order.client_payment_records(),
        )
        return TemplateResponse(
            request, "Orders/ClientNewPayment.html", context
        )

    def remove_personnel_payment_record(self, request, object_id, payment_id):
        order = Orders.models.Order.objects.get(id=object_id)
        payment_record = Financial.models.OutgoingPayment.objects.filter(
            id=payment_id
        )
        if payment_record:
            payment_record.delete()
            order.refresh_order_payment_statuses()
            messages.add_message(
                request,
                messages.SUCCESS,
                message=fm.order_remove_personnel_payment_record_success,
            )
        else:
            messages.add_message(
                request,
                messages.WARNING,
                message=fm.order_remove_personnel_payment_record_not_found,
            )
        return redirect(
            reverse("admin:order_personnel_payment", args=(object_id,))
        )

    def new_personnel_payment(self, request, object_id):
        order = Orders.models.Order.objects.get(id=object_id)
        if request.method == "POST":
            form = Orders.forms.OrderClientPaymentForm(request.POST)
            if form.is_valid():
                data = utils.map_to_model_data(
                    form.cleaned_data,
                    [
                        ("paid_at",),
                        ("new_payment_amount", "paid_amount"),
                        ("description", "payment_desc"),
                    ],
                )
                data["to_user"] = order.assigned_personnel
                data["order"] = order

                try:
                    Financial.models.OutgoingPayment.objects.create(**data)
                    order.refresh_order_payment_statuses()
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        message=fm.order_personnel_payment_success,
                    )
                except Exception as e:
                    messages.add_message(
                        request, messages.ERROR, message=e.__str__()
                    )
                finally:
                    return redirect(
                        reverse(
                            "admin:order_personnel_payment", args=(object_id,)
                        )
                    )

        form = Orders.forms.OrderClientPaymentForm(
            initial=dict(
                remaining_amount=order.personnel_remaining_payable,
                new_payment_amount=order.personnel_remaining_payable,
                paid_at=utils.current_date_str(),
            )
        )
        context = dict(
            self.admin_site.each_context(request),
            form=form,
            order=order,
            payment_records=order.personnel_payment_records(),
        )
        return TemplateResponse(
            request, "Orders/PersonnelNewPayment.html", context
        )

    @admin.display(description="خدمت")
    def display_service_card(self, obj):
        return utils.beautify_string_cut(str(obj))

    @admin.display(description="هزینه کل خدمت (بدون تخفیف)")
    def display_total_order_cost(self, obj):
        return utils.put_comma_for_numbers(obj.total_order_cost)

    @admin.display(description="تخفیف")
    def display_discount_cost(self, obj):
        return utils.put_comma_for_numbers(obj.discount)

    @admin.display(description="")
    def display_custom_actions(self, obj):
        client_payment_link = reverse(
            "admin:order_client_payment", args=[obj.id]
        )
        personnel_payment_link = reverse(
            "admin:order_personnel_payment", args=[obj.id]
        )

        return mark_safe(
            f"<a href={client_payment_link} target='blank'>پرداخت "
            f"کارفرما</a><br/>"
            f"<a href={personnel_payment_link} target='blank'>پرداخت پرسنل</a>"
        )
