from django.db import models

from BasicInfo.models import CatalogCallReason, CatalogCallReferral
from common import field_choices
from Orders.models import CareContract, Client, Order
from Personnel.models import Personnel


class Call(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    call_type = models.CharField(
        max_length=3,
        choices=field_choices.CallTypeChoices.choices,
        default=field_choices.CallTypeChoices.INCOMING,
        verbose_name="ورودی یا خروجی",
    )

    status = models.CharField(
        max_length=3,
        choices=field_choices.CallAnswerStatusChoices.choices,
        default=field_choices.CallAnswerStatusChoices.ANSWERED,
        verbose_name="وضعیت پاسخ",
    )

    reason = models.ForeignKey(
        CatalogCallReason,
        on_delete=models.CASCADE,
        verbose_name="علت تماس",
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="خدمت موردی مربوطه",
    )

    contract = models.ForeignKey(
        CareContract,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="قرارداد مربوطه",
    )

    note = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name="یادداشت",
        help_text="در صورتی که یادداشت برای تماس های مرتبط با یک سرویس ثبت شود"
        "به صورت خودکار یادداشت به قسمت یادداشت(کامنت) های سرویس هم اضافه میشود",
    )

    class Meta:
        abstract = True


class PersonnelCall(Call):
    personnel = models.ForeignKey(
        Personnel, on_delete=models.CASCADE, verbose_name="پرسنل"
    )

    class Meta:
        verbose_name = "تماس پرسنل"
        verbose_name_plural = "تماس های پرسنل"

    def __str__(self) -> str:
        return "تماس از طرف %s" % self.personnel


class ClientCall(Call):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="کارفرما",
        help_text="برای جست جوی در شماره های تماس کارفرما از این فیلد "
        "استفاده کنید",
    )

    raw_phone_number = models.CharField(
        max_length=11,
        null=True,
        blank=True,
        verbose_name="شماره تماس",
        help_text="در صورتی که شماره در لیست مخاطبین وجود نداشت از این فیلد "
        "استفاده کنید",
    )

    referral = models.ForeignKey(
        CatalogCallReferral,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="معرف",
    )

    class Meta:
        verbose_name = "تماس کارفرما و دیگران"
        verbose_name_plural = "تماس های کارفرما و دیگران"

    def __str__(self) -> str:
        msg = self.client.full_name if self.client else self.raw_phone_number
        return "تماس از طرف %s" % msg
