from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from common import field_choices, fields, validators


class Lookup(models.Model):
    title = models.CharField(max_length=50, verbose_name="عنوان")
    note = models.TextField(null=True, blank=True, verbose_name="یادداشت")
    code = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class CatalogCallReason(Lookup):
    class Meta:
        verbose_name = "علت تماس"
        verbose_name_plural = "علت های تماس"


class CatalogCallReferral(Lookup):
    class Meta:
        verbose_name = "نوع معرف"
        verbose_name_plural = "انواع معرف"


class CatalogArea(Lookup):
    category = models.CharField(
        choices=field_choices.AreaChoices.choices,
        max_length=3,
        verbose_name="دسته بندی",
    )

    class Meta:
        verbose_name = "محدوده مکانی"
        verbose_name_plural = "محدوده های مکانی"


class CatalogService(Lookup):
    parent = models.ForeignKey(
        "CatalogService",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="سرویس مادر",
        help_text="در صورتی که سرویس جدید زیر مجموعه سرویس دیگری است این قسمت را پر کنید",
    )

    healthcare_franchise = models.PositiveSmallIntegerField(
        default=70,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="سهم مرکز",
        help_text="به درصد است",
    )
    base_price = fields.ToomanField(default=0, verbose_name="قیمت پایه سرویس")

    class Meta:
        verbose_name = "سرویس"
        verbose_name_plural = "سرویس ها"

    @property
    def is_leaf(self):
        qs = CatalogService.objects.filter(parent=self)
        return not bool(qs)

    def __str__(self):
        parent_hirearchy = self.parent or ""
        return f"{self.title} > {parent_hirearchy}"


class CatalogPersonnelRole(Lookup):
    class Meta:
        verbose_name = "نقش پرسنل"
        verbose_name_plural = "نقش های پرسنل"


class CatalogTagSpecificationCategory(Lookup):
    class Meta:
        verbose_name = " دسته بندی ویژگی (تگ)"
        verbose_name_plural = "دسته بندی های ویژگی های تگ"


class CatalogTagSpecification(Lookup):
    category = models.ForeignKey(
        "CatalogTagSpecificationCategory",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="دسته بندی",
    )
    for_who = models.CharField(
        choices=field_choices.ForPartyTypeChoices.choices,
        max_length=3,
        verbose_name="قابل استفاده برای",
    )

    def __str__(self):
        return f"{self.category or 'بدون دسته بندی'} | {self.title}"

    class Meta:
        verbose_name = "ویژگی (تگ)"
        verbose_name_plural = "تگ ها"


class CatalogValuedSpecificationCategory(Lookup):
    class Meta:
        verbose_name = "دسته بندی ویژگی مقداری"
        verbose_name_plural = "دسته بندی  های ویژگی های مقداری"


class CatalogValuedSpecification(Lookup):
    category = models.ForeignKey(
        "CatalogValuedSpecificationCategory",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="دسته بندی",
    )
    for_who = models.CharField(
        choices=field_choices.ForPartyTypeChoices.choices,
        max_length=3,
        verbose_name="برای",
    )

    def __str__(self):
        return f"{self.for_who} | {self.category} | {self.title}"

    class Meta:
        verbose_name = "ویژگی مقداری"
        verbose_name_plural = "ویژگی های مقداری"


class CatalogMedicalCenter(Lookup):
    phone_number = models.CharField(
        max_length=20,
        validators=[validators.telephone_number],
        null=True,
        blank=True,
        verbose_name="شماره همراه",
    )

    class Meta:
        verbose_name = "مرکز همکار"
        verbose_name_plural = "مراکز همکار"


class WeekDay(Lookup):
    class Meta:
        verbose_name = "روز هفته"
        verbose_name_plural = "روز های هفته"


class Person(models.Model):
    first_name = models.CharField(
        max_length=50, validators=[validators.trim_string], verbose_name="نام"
    )
    last_name = models.CharField(
        max_length=50,
        validators=[validators.trim_string],
        verbose_name="نام خانوادگی",
    )

    gender = models.CharField(
        max_length=1,
        choices=field_choices.GenderChoices.choices,
        verbose_name="جنسیت",
    )

    national_code = models.CharField(
        max_length=10,
        validators=[
            validators.national_code,
            validators.blacklist_national_codes,
        ],
        verbose_name="کد ملی",
        null=True,
        blank=True,
    )

    birthdate = models.DateField(
        null=True, blank=True, verbose_name="تاریخ تولد"
    )

    class Meta:
        abstract = True

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name
