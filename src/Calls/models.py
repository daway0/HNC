from django.db import models

from BasicInfo.models import CatalogCallReason, CatalogCallReferral
from Orders.models import CareContract, Client, Order
from Personnel.models import Personnel

# OUT OF CODE (DB)
# class ReasonChoices(models.TextChoices):
#     CONSULTATION = "", ...
#     SERVICE_FEEDBACK = ...
#     ORDER = ...
#     WRONG_NUMBER = ...
#     RECRUITMENT = ...

# class ReferralChoices(models.TextChoices):
#     WEBSITE = ...
#     FRIEND = ...
#     AD1 = ...
#     AGENCY = ...


# Create your models here.


class Call(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class CallTypeChoices(models.TextChoices):
        INCOMING = "INC", "ورودی"
        OUTGOING = "OUT", "خروجی"

    call_type = models.CharField(
        max_length=3,
        choices=CallTypeChoices.choices,
        default=CallTypeChoices.INCOMING,
        verbose_name="ورودی یا خروجی",
    )

    class StatusChoices(models.TextChoices):
        ANSWERED = "ANS", "پاسخ داده شده"
        NOT_ANSWERED = "REJ", "رد شده"

    status = models.CharField(
        max_length=3,
        choices=StatusChoices.choices,
        default=StatusChoices.ANSWERED,
        verbose_name="وضعیت پاسخ",
    )

    reason = models.ForeignKey(
        CatalogCallReason,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
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
        help_text="برای جست جوی در شماره های تماس کارفرما از این فیلد " "استفاده کنید",
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
