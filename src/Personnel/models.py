from django.db import models

from BasicInfo.models import (
    CatalogArea,
    CatalogPersonnelRole,
    CatalogTagSpecification,
    CatalogValuedSpecification,
    Person,
)


class PersonnelValuedSpecification(models.Model):
    specification = models.ForeignKey(
        CatalogValuedSpecification,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="ویژگی مقداری",
    )
    personnel = models.ForeignKey(
        "Personnel", on_delete=models.SET_NULL, null=True
    )
    value = models.CharField(max_length=250, verbose_name="مقدار")

    class Meta:
        pass


class Personnel(Person):
    phone_number = models.CharField(
        max_length=11, verbose_name="شماره تلفن همراه"
    )

    role = models.ForeignKey(
        CatalogPersonnelRole,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="نقش پرسنل",
    )

    address = models.CharField(
        max_length=250, null=True, blank=True, verbose_name="آدرس"
    )

    card_number = models.CharField(
        max_length=16, null=True, blank=True, verbose_name="شماره کارت بانکی"
    )

    contract_date = models.DateField(
        null=True, verbose_name="تاریخ شروع همکاری"
    )
    end_contract_date = models.DateField(
        null=True, blank=True, verbose_name="تاریخ پایان همکاری"
    )

    areas = models.ManyToManyField(CatalogArea, verbose_name="محدوده ها")

    class PersonnelStatusChoices(models.TextChoices):
        IDLE = "IDLE", "Ready"
        IN_PROGRESS = "PRGS", "In progress"

        # taraf dg ba markaz kar nemikone
        INACTIVE = "IACT", "In active"

    status = models.CharField(
        choices=PersonnelStatusChoices.choices,
        max_length=4,
        default=PersonnelStatusChoices.IDLE,
        verbose_name="وضعیت",
    )
    # masalan chera taraf deactive shode ro benevisim, ya masalan taraf 2
    # mah nist ya har chizi
    last_status_note = models.TextField(
        null=True, blank=True, verbose_name="یادداشت آخرین وضعیت پرسنل"
    )

    # PartyMetaData
    # metadata = models.JSONField()

    tag_specifications = models.ManyToManyField(
        to=CatalogTagSpecification, verbose_name="تگ"
    )

    valued_specifications = models.ManyToManyField(
        through=PersonnelValuedSpecification,
        to=CatalogValuedSpecification,
        verbose_name="مهارت",
    )
    note = models.TextField(
        null=True, blank=True, verbose_name="یادداشت درباره پرسنل"
    )

    class Meta:
        verbose_name = "پرسنل"
        verbose_name_plural = "پرسنل"

    @property
    def last_service(self) -> models.DateTimeField: ...

    @property
    def last_month_services_count(self) -> int: ...

    @property
    def rate(self) -> float:
        # az resume gerefte mishe
        ...

    def __str__(self):
        return " ".join([self.full_name, f"({self.role.title})"])
