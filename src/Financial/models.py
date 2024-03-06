from django.db import models
from Orders.models import (
    Order,
    CareContract,
    Client
)
from Personnel.models import Personnel


class Payment(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="زمان پرداخت"
    )

    paid_at = models.CharField(max_length=10)

    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="خدمت موردی مربوطه",
    )
    paid_amount = models.PositiveBigIntegerField(verbose_name="مبلغ پرداختی")

    contract = models.ForeignKey(
        CareContract,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="قرارداد مربوطه",
    )

    to_card_number = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        verbose_name="شماره کارت مقصد",
    )

    payment_desc = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = "پرداختی"
        verbose_name_plural = "پرداختی ها"


    @property
    def payment_type(self):
        # incoming and outgoing
        ...



class IncomingPayment(Payment):
    from_user = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name="از طرف",
    )

    class Meta:
        verbose_name = "پرداخت کارفرما"
        verbose_name_plural = "پرداختی های کارفرما"


class OutgoingPayment(Payment):
    to_user = models.ForeignKey(
        Personnel,
        on_delete=models.CASCADE,
        verbose_name="به شخص",
    )
    class Meta:
        verbose_name = "پرداخت پرسنل"
        verbose_name_plural = "پرداختی های پرسنل"
