from django import forms
from jalali_date.admin import AdminJalaliDateWidget
from jalali_date.fields import JalaliDateField

from . import models


class PersonnelForm(forms.ModelForm):

    contract_date = JalaliDateField(
        widget=AdminJalaliDateWidget, label="تاریخ شروع همکاری", required=False
    )
    end_contract_date = JalaliDateField(
        widget=AdminJalaliDateWidget,
        label="تاریخ پایان همکاری",
        required=False,
    )
    birthdate = JalaliDateField(
        widget=AdminJalaliDateWidget, label="تاریخ تولد", required=False
    )

    class Meta:
        model = models.Personnel
        fields = "__all__"
