from django import forms
from django.core.exceptions import ValidationError

from . import models as m


class OrderPaymentForm(forms.Form):
    remaining_amount = forms.IntegerField(
        disabled=True,
        required=False,
        label="قابل پرداخت",
    )
    new_payment_amount = forms.IntegerField(
        label="پرداختی جدید",
    )
    paid_at = forms.CharField(
        label="تاریخ پرداخت",
    )

    description = forms.CharField(
        label="توضیحات", required=False, widget=forms.Textarea
    )


class OrderClientPaymentForm(OrderPaymentForm): ...


class OrderPersonnelPaymentForm(OrderPaymentForm):
    ...

    # def clean(self):
    #     if self.cleaned_data['new_payment_amount'] > self.cleaned_data['remaining_amount']:
    #         raise ValidationError("یی")

    # def clean_payment_amount(self):
    #     if self.cleaned_data['payment_amount'] < 2:
    #         raise ...

    # def clean_email(self):
    #     # Custom validation logic for email field
    #     email = self.cleaned_data['email']
    #     # Check for something specific in the email
    #     if not email.endswith('@example.com'):
    #         raise forms.ValidationError('Email must end with @example.com')
    #     return email


def is_hour_valid(hour: int) -> bool:
    try:
        return 0 < hour < 25
    except TypeError:
        return False


class CareContractForm(forms.ModelForm):
    class Meta:
        model = m.CareContract
        fields = [
            "referral",
            "referral_personnel",
            "referral_client",
            "referral_other_healthcare",
            "care_for",
            "patients",
            "shift",
            "shift_days",
            "shift_start",
            "shift_end",
            "client",
            "relationship_with_patient",
            "relationship_with_patient_note",
            "service_location",
            "start",
            "end",
            "personnel",
            "include_holidays",
            "personnel_monthly_salary",
            "personnel_salary_payment_time",
            "healthcare_franchise_amount",
            "client_payment_status",
            "personnel_payment_status",
        ]

    def _validate_relations(self):
        relationship_with_patient = self.cleaned_data.get(
            "relationship_with_patient"
        )
        relationship_with_patient_note = self.cleaned_data.get(
            "relationship_with_patient_note"
        )
        if relationship_with_patient and relationship_with_patient_note:
            raise ValidationError(
                ("در صورت ارائه نسبت با بیمار، احتیاج به نوشتن توضیحات نیست."),
            )

    def _validate_shifts(self):
        shift_start = self.cleaned_data.get("shift_start")
        shift_end = self.cleaned_data.get("shift_end")
        if not (is_hour_valid(shift_start) and is_hour_valid(shift_end)):
            raise ValidationError(
                ("ساعت شروع و پایان شیفت صحیح نمی‌باشد: %(value)r"),
                params={"value": (shift_start, shift_end)},
            )

    def _validate_contract_duration(self):
        invalid_duration_exception = ValidationError(
            "حداقل طول قرارداد 1 ماه می‌باشد."
        )
        start = self.cleaned_data.get("start")
        end = self.cleaned_data.get("end")
        if not (start and end):
            return

        if start.day == 1:
            if not (end.day - start.day) >= 28:
                raise invalid_duration_exception
        else:
            if abs((end.day - start.day)) > 2:
                raise invalid_duration_exception

    def _validate_personnel_salary(self):
        if not (
            personnel_monthly_salary := self.cleaned_data.get(
                "personnel_monthly_salary"
            )
        ):
            return

        if personnel_monthly_salary < 0:
            raise ValidationError(
                "مقدار دستمزد پرسنل صحیح نمی‌باشد: %(value)r",
                params={"value": personnel_monthly_salary},
            )

    def _validate_healthcare_franchise_amount(self):
        if not (
            healthcare_franchise_amount := self.cleaned_data.get(
                "healthcare_franchise_amount"
            )
        ):
            return

        if healthcare_franchise_amount < 0:
            raise ValidationError(
                "مقدار دستمزد پرسنل صحیح نمی‌باشد: %(value)r",
                params={"value": healthcare_franchise_amount},
            )

    def clean(self):
        super().clean()
        self._validate_relations()
        self._validate_shifts()
        self._validate_contract_duration()
        self._validate_personnel_salary()
        self._validate_healthcare_franchise_amount()


class OrderForm(forms.ModelForm):
    class Meta:
        model = m.Order
        fields = [
            "referral",
            "referral_personnel",
            "referral_client",
            "referral_other_healthcare",
            "client",
            "service_location",
            "patient_tag_specifications",
            "accepted",
            "done",
            "assigned_personnel",
            "order_status",
            "client_payment_status",
            "personnel_payment_status",
            "discount",
        ]

    def clean(self):
        super().clean()
