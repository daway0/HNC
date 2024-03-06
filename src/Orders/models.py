from BasicInfo.models import (
    CatalogCallReferral,
    CatalogMedicalCenter,
    CatalogService,
    CatalogTagSpecification,
    Junction,
    Person,
    WeekDay,
)
from django.db import models as m
from django.db.models import QuerySet, Sum
from Patients.models import Patient
from Personnel.models import Personnel

from utils import beautify_string_cut


class Client(Person):
    class Meta:
        verbose_name = "کارفرما"
        verbose_name_plural = "کارفرما ها"


class ClientPhoneNumber(m.Model):
    client = m.ForeignKey(Client, on_delete=m.CASCADE, verbose_name="کارفرما")

    class NumberTypeChoices(m.TextChoices):
        NORMAL = "N", "شماره تماس عادی"
        EMERGENCY = "E", "شماره تماس اضطراری"

    number_type = m.CharField(
        choices=NumberTypeChoices.choices,
        default=NumberTypeChoices.NORMAL,
        max_length=1,
        verbose_name="نوع شماره",
    )

    phone_number = m.CharField(max_length=11, verbose_name="شماره تلفن همراه")

    added_at = m.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "شماره تماس"
        verbose_name_plural = "شماره های تماس"

    def __str__(self):
        return f"{self.client.full_name} {self.phone_number}"


class ClientAddress(m.Model):
    client = m.ForeignKey(Client, on_delete=m.CASCADE)
    location_text = m.CharField(max_length=250, verbose_name="آدرس")

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس ها"

    def __str__(self):
        return f"{self.client.full_name} {self.location_text}"


class Referral(m.Model):
    referral = m.ForeignKey(
        CatalogCallReferral,
        on_delete=m.CASCADE,
        verbose_name="نوع معرفی",
        null=True,
        blank=True,
    )

    referral_personnel = m.ForeignKey(
        Personnel,
        on_delete=m.CASCADE,
        verbose_name="همکار معرف",
        null=True,
        blank=True,
        related_name="personnel_%(class)s_referral",
    )
    referral_client = m.ForeignKey(
        Client,
        on_delete=m.CASCADE,
        verbose_name="کارفرما معرف",
        null=True,
        blank=True,
        related_name="client_%(class)s_referral",
    )
    referral_other_healthcare = m.ForeignKey(
        CatalogMedicalCenter,
        on_delete=m.CASCADE,
        verbose_name="مرکز همکار معرف",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class PaymentStatusChoices(m.TextChoices):
    PARTIAL_PAID = "PAPD", "پرداخت جزیی"
    COMPLETE_PAID = "COPD", "پرداخت کامل"
    NOT_PAID = "NOPD", "پرداخت نشده"


class Order(Referral):
    client = m.ForeignKey(
        Client,
        on_delete=m.CASCADE,
        verbose_name="کارفرما",
        related_name="orders",
    )
    service_location = m.ForeignKey(
        ClientAddress, on_delete=m.CASCADE, verbose_name="محل خدمت"
    )
    patient_tag_specifications = m.ManyToManyField(
        CatalogTagSpecification,
        blank=True,
        verbose_name="خصوصیات درخواست دهنده",
    )

    # initiated by system (when operator makes new service record)
    requested = m.DateTimeField(auto_now_add=True, verbose_name="زمان درخواست")

    # by nurse
    accepted = m.DateTimeField(
        null=True, blank=True, verbose_name="زمان قبول درخواست توسط پرسنل"
    )

    # when nurse called
    done = m.DateTimeField(null=True, blank=True, verbose_name="زمان اتمام")

    assigned_personnel = m.ForeignKey(
        Personnel,
        on_delete=m.SET_NULL,
        null=True,
        blank=True,
        verbose_name="پرسنل",
        related_name="services",
    )

    class StatusChoices(m.TextChoices):
        DONE = "DON", "انجام شده"
        ASSIGNED = "ASG", "محول شده"
        WAIT_LISTED = "WLS", "لیست انتظار"

        CANCELED = "CPT", "لغو شده"

    order_status = m.CharField(
        choices=StatusChoices.choices,
        max_length=3,
        default=StatusChoices.WAIT_LISTED,
        verbose_name="وضعیت درخواست",
    )

    # READ ONLY (CHANGE BY ACTIONS )
    client_payment_status = m.CharField(
        max_length=4,
        choices=PaymentStatusChoices.choices,
        default=PaymentStatusChoices.NOT_PAID,
        verbose_name="وضعیت پرداخت کارفرما",
    )

    # READ ONLY (CHANGE BY ACTIONS )
    personnel_payment_status = m.CharField(
        max_length=4,
        choices=PaymentStatusChoices.choices,
        default=PaymentStatusChoices.NOT_PAID,
        verbose_name="وضعیت پرداخت پرسنل",
    )

    referral = m.ForeignKey(
        CatalogCallReferral,
        on_delete=m.CASCADE,
        verbose_name="معرف",
        null=True,
        blank=True,
    )

    referral_personnel = m.ForeignKey(
        Personnel,
        on_delete=m.CASCADE,
        verbose_name="همکار معرف",
        null=True,
        blank=True,
        related_name="personnel_orders_referral",
    )
    referral_client = m.ForeignKey(
        Client,
        on_delete=m.CASCADE,
        verbose_name="کارفرما معرف",
        null=True,
        blank=True,
        related_name="client_orders_referral",
    )
    referral_other_healthcare = m.ForeignKey(
        CatalogMedicalCenter,
        on_delete=m.CASCADE,
        verbose_name="مرکز همکار معرف",
        null=True,
        blank=True,
    )
    discount = m.IntegerField(default=0, verbose_name="تخفیف", help_text="به تومان")

    class Meta:
        verbose_name = "خدمت موردی"
        verbose_name_plural = "خدمات موردی"

    @property
    def personnel_share(self):
        """in tooman"""
        order_services = OrderService.objects.filter(order=self)
        personnel_share = 0
        for order_service in order_services:
            personnel_franchise = 100 - order_service.service.healthcare_franchise
            personnel_share += (order_service.cost * personnel_franchise) / 100
        return personnel_share

    @property
    def total_order_cost(self):
        services = OrderService.objects.filter(order=self)
        if services:
            return services.aggregate(total_order_cost=Sum("cost"))["total_order_cost"]
        return 0

    @property
    def total_order_cost_after_discount(self):
        if not self.total_order_cost == 0:
            return self.total_order_cost - self.discount
        return 0

    @property
    def services(self) -> str:
        services_list = OrderService.objects.filter(order=self).values_list(
            "service__title", flat=True
        )
        if services_list:
            return beautify_string_cut(", ".join(services_list))
        return "(بدون سرویس)"

    @property
    def client_remaining_payable(self):
        from Financial import models as FinancialModels

        client_payments = FinancialModels.IncomingPayment.objects.filter(order=self)

        if not client_payments:
            return self.total_order_cost_after_discount

        payed = client_payments.aggregate(payed_by_now=Sum("paid_amount"))[
            "payed_by_now"
        ]
        remaining = self.total_order_cost_after_discount - payed
        return remaining

    @property
    def personnel_remaining_payable(self):
        from Financial import models as FinancialModels

        personnel_payments = FinancialModels.OutgoingPayment.objects.filter(order=self)

        if not personnel_payments:
            return self.personnel_share

        payed = personnel_payments.aggregate(payed_by_now=Sum("paid_amount"))[
            "payed_by_now"
        ]
        remaining = self.personnel_share - payed
        return remaining

    def client_payment_records(self) -> QuerySet:
        from Financial import models as FinancialModels

        return FinancialModels.IncomingPayment.objects.filter(order=self)

    def personnel_payment_records(self) -> QuerySet:
        from Financial import models as FinancialModels

        return FinancialModels.OutgoingPayment.objects.filter(order=self)

    def refresh_order_payment_statuses(self) -> None:
        self._refresh_order_personnel_payment_status()
        self._refresh_order_client_payment_status()

    def _refresh_order_client_payment_status(self) -> None:
        if self.client_remaining_payable <= 0:
            self.client_payment_status = PaymentStatusChoices.COMPLETE_PAID
        elif self.client_remaining_payable == self.total_order_cost_after_discount:
            self.client_payment_status = PaymentStatusChoices.NOT_PAID
        else:
            self.client_payment_status = PaymentStatusChoices.PARTIAL_PAID
        self.save()

    def _refresh_order_personnel_payment_status(self) -> None:
        if self.personnel_remaining_payable <= 0:
            self.personnel_payment_status = PaymentStatusChoices.COMPLETE_PAID

        elif self.personnel_remaining_payable == self.personnel_share:
            self.personnel_payment_status = PaymentStatusChoices.NOT_PAID

        else:
            self.personnel_payment_status = PaymentStatusChoices.PARTIAL_PAID
        self.save()

    def __str__(self):
        return f"{self.client.full_name}" f" ({self.services})"


class OrderService(Junction):
    order = m.ForeignKey(Order, on_delete=m.CASCADE, verbose_name="خدمت موردی")
    service = m.ForeignKey(CatalogService, on_delete=m.CASCADE, verbose_name="سرویس")
    cost = m.IntegerField(default=0, verbose_name="هزینه", help_text="به تومان")

    created_at = m.DateTimeField(auto_now_add=True)
    updated_at = m.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.service.id}_{self.order.id}_{self.id}"

    class Meta:
        verbose_name = "سرویس خدمت موردی"
        verbose_name_plural = "سرویس های خدمت موردی"


class Comment(m.Model):
    comment = m.CharField(max_length=250, verbose_name="کامنت")
    created_at = m.DateTimeField(auto_now_add=True)
    updated_at = m.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.id}"


class OrderComment(Comment):
    order = m.ForeignKey(
        Order, on_delete=m.SET_NULL, null=True, verbose_name="خدمت موردی"
    )

    class Meta:
        verbose_name = " کامنت سفارش"
        verbose_name_plural = "کامنت های سفارش"


class ContractComment(Comment):
    contract = m.ForeignKey(
        "CareContract", on_delete=m.SET_NULL, null=True, verbose_name="قراردار"
    )

    class Meta:
        verbose_name = " کامنت قرارداد"
        verbose_name_plural = "کامنت های قرارداد"


class CareContract(Referral):
    class TypeChoices(m.TextChoices):
        ELDER = "E", "سالمند"
        PATIENT = "P", "مددجو"
        KID = "K", "کودک"

    care_for = m.CharField(
        choices=TypeChoices.choices, max_length=1, verbose_name="مراقبت از"
    )

    patients = m.ManyToManyField(Patient, verbose_name="مددجو/ سالمند/ کودک")

    class ShiftOrderChoices(m.TextChoices):
        DAY = "D", "روزانه"
        NIGHT = "N", "شبانه"
        BOTH = "B", "شبانه روزی"
        OTHER = "O", "سایر"

    shift = m.CharField(
        choices=ShiftOrderChoices.choices, max_length=1, verbose_name="شیفت"
    )

    shift_days = m.ManyToManyField(WeekDay, verbose_name="روز های شیفت")

    shift_start = m.PositiveSmallIntegerField(default=8, verbose_name="ساعت شروع شیفت")
    shift_end = m.PositiveSmallIntegerField(default=18, verbose_name="ساعت پایان شیفت")

    client = m.ForeignKey(Client, on_delete=m.CASCADE, verbose_name="کارفرما")

    class RelationShipChoices(m.TextChoices):
        SELF = "S", "خودشان"
        CHILD = "C", "فرزند"
        PARTNER = "P", "همسر"
        OTHER = "O", "سایر"

    relationship_with_patient = m.CharField(
        choices=RelationShipChoices.choices,
        max_length=1,
        verbose_name="نسبت با بیمار",
    )
    relationship_with_patient_note = m.CharField(
        max_length=150,
        null=True,
        verbose_name="نسبت با بیمار",
        blank=True,
        help_text="در صورتی که رابطه با فرد متقاضی خدمت سایر "
        "بود، نسبت دقیق آنها در این فیلد نوشته شود.",
    )
    service_location = m.ForeignKey(
        ClientAddress, on_delete=m.CASCADE, verbose_name="محل خدمت"
    )

    start = m.DateTimeField(verbose_name="شروع قرارداد")
    end = m.DateTimeField(verbose_name="پایان قرارداد")

    @property
    def duration_in_hours(self) -> int:
        return ...

    personnel = m.ForeignKey(Personnel, on_delete=m.CASCADE, verbose_name="پرسنل")

    include_holidays = m.BooleanField(
        default=True,
        verbose_name="شامل تعطیلات می شود",
        help_text="در تعطیلات رسمی از طرف هیات دولت پرسنل تعطیل نمی باشند",
    )

    personnel_monthly_salary = m.IntegerField(
        default=0,
        verbose_name="حقوق ماهانه پرسنل",
    )

    class PaymentTimeChoices(m.TextChoices):
        START = "S", "ابتدای ماه"
        END = "E", "انتهای ماه"
        OTHER = "O", "سایر"

    personnel_salary_payment_time = m.CharField(
        choices=PaymentTimeChoices.choices,
        verbose_name="تسویه با پرسنل",
        max_length=1,
    )

    healthcare_franchise_amount = m.IntegerField(
        default=0,
        verbose_name="فرانشیز مرکز",
        help_text="مبلغ فرانشیز مرکز به تومان",
    )

    # READ ONLY (CHANGE BY ACTIONS )
    client_payment_status = m.CharField(
        max_length=4,
        verbose_name="وضعیت تسفیه حساب کارفرما",
        choices=PaymentStatusChoices.choices,
        default=PaymentStatusChoices.NOT_PAID,
    )

    # READ ONLY (CHANGE BY ACTIONS )
    personnel_payment_status = m.CharField(
        max_length=4,
        verbose_name="وضعیت تسفیه حساب پرسنل",
        choices=PaymentStatusChoices.choices,
        default=PaymentStatusChoices.NOT_PAID,
    )

    @property
    def need_salary_increment(self) -> bool: ...

    class Meta:
        verbose_name = "قرار داد مراقبت"
        verbose_name_plural = "قرارداد های مراقبت"

    def __str__(self):
        return "قرارداد مراقبت با %s" % self.client
