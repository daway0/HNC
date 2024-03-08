import re

from django import forms
from django.core.exceptions import ValidationError

from Personnel import models as m





class PersonnelForm(forms.ModelForm):
    class Meta:
        model = m.Personnel
        fields = [
            "first_name",
            "last_name",
            "gender",
            "national_code",
            "birthdate",
            "phone_number",
            "role",
            "address",
            "card_number",
            "contract_date",
            "end_contract_date",
            "areas",
        ]

    def clean_national_code(self):
        if not (national_code := self.cleaned_data.get("national_code")):
            return

        if not re.match(r"^[0-9]{10}$", national_code):
            raise ValidationError(
                "کد ملی صحیح نمی‌باشد: %(v)r", params={"v": national_code}
            )
        return national_code

    def clean_phone_number(self):
        if not (phone_number := self.cleaned_data.get("phone_number")):
            return

        if not re.match(r"^[0-9]{11}$", phone_number):
            raise ValidationError(
                "شماره تلفن صحیح نمی‌باشد: %(v)r", params={"v": phone_number}
            )
        return phone_number

    def clean_card_number(self):
        if not (card_number := self.cleaned_data.get("card_number")):
            return

        if not re.match(r"^[0-9]{16}$", card_number):
            raise ValidationError(
                "شماره کارت صحیح نمی‌باشد: %(v)r", params={"v": card_number}
            )
        return card_number

    def validate_contract(self):
        contract_date = self.cleaned_data.get("contract_date")
        end_contract_date = self.cleaned_data.get("end_contract_date")
        if not (contract_date and end_contract_date):
            return

        if contract_date > end_contract_date:
            _err_msg = "تاریخ همکاری وارد شده صحیح نمی‌باشد."
            self.add_error("contract_date", _err_msg)
            self.add_error("end_contract_date", _err_msg)

    def clean(self):
        super().clean()
        self.validate_contract()
