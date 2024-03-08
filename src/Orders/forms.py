from django import forms
from jalali_date.admin import AdminJalaliDateWidget
from jalali_date.fields import JalaliDateField


class OrderPaymentForm(forms.Form):
    remaining_amount = forms.IntegerField(
        disabled=True,
        required=False,
        label="قابل پرداخت",
    )
    new_payment_amount = forms.IntegerField(label="پرداختی جدید")
    paid_at = JalaliDateField(
        label="تاریخ پرداخت", widget=AdminJalaliDateWidget
    )

    description = forms.CharField(
        label="توضیحات", required=False, widget=forms.Textarea
    )


class OrderClientPaymentForm(OrderPaymentForm): ...


class OrderPersonnelPaymentForm(OrderPaymentForm): ...
