from django import forms


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
