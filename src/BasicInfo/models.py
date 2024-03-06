from django.db import models


class Junction(models.Model):
    pass


class Lookup(models.Model):
    title = models.CharField(max_length=50, verbose_name="عنوان")
    note = models.TextField(null=True, blank=True, verbose_name="یادداشت")

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


class Person(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="نام")
    last_name = models.CharField(max_length=50, verbose_name="نام خانوادگی")

    class GenderChoices(models.TextChoices):
        MALE = "M", "مرد"
        FEMALE = "F", "زن"

    gender = models.CharField(
        max_length=1, choices=GenderChoices.choices, verbose_name="جنسیت"
    )

    national_code = models.CharField(
        max_length=10, verbose_name="کد ملی", null=True, blank=True
    )

    birthdate = models.DateField(null=True, blank=True, verbose_name="تاریخ تولد")

    class Meta:
        abstract = True

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class CatalogArea(Lookup):
    class AreaChoices(models.TextChoices):
        # mantaqe1, mantaqe2, ...
        DISTRICT = "DIS", "منطقه"

        # pasdaran, iranshahr
        NEIGHBORHOOD = "NGB", "محله"

        # SHOMAL, JONUB, SHARQ, QARB
        AREA = "ARE", "محدوده"

    category = models.CharField(
        choices=AreaChoices.choices, max_length=3, verbose_name="دسته بندی"
    )

    class Meta:
        verbose_name = "محدوده مکانی"
        verbose_name_plural = "محدوده های مکانی"


class CatalogServiceCategory(Lookup):
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="دسته بندی",
    )


class CatalogService(Lookup):
    parent = models.ForeignKey(
        "CatalogService", null=True, blank=True, on_delete=models.SET_NULL
    )
    category_tree = models.CharField(max_length=250, null=True, blank=True)
    healthcare_franchise = models.PositiveSmallIntegerField(
        default=100, verbose_name="سهم مرکز"
    )
    base_price = models.IntegerField(default=0, verbose_name="قیمت پایه سرویس")

    class Meta:
        verbose_name = "سرویس"
        verbose_name_plural = "سرویس ها"


class CatalogPersonnelRole(Lookup):
    class Meta:
        verbose_name = "نقش پرسنل"
        verbose_name_plural = "نقش های پرسنل"


class CatalogTagSpecificationCategory(Lookup):
    class Meta:
        verbose_name = " دسته بندی ویژگی (تگ)"
        verbose_name_plural = "دسته بندی های ویژگی های تگ"


class ForPartyTypeChoices(models.TextChoices):
    PERSONNEL = "PRS", "پرسنل"
    PATIENT = "PTN", "بیمار"
    CLIENT = "CLI", "کارفرما"
    COMMON = "CMN", "مشترک بین همه"


class CatalogTagSpecification(Lookup):
    category = models.ForeignKey(
        "CatalogTagSpecificationCategory",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="دسته بندی",
    )
    for_who = models.CharField(
        choices=ForPartyTypeChoices.choices, max_length=3, verbose_name="برای"
    )

    def __str__(self):
        return f"{self.category} | {self.title}"

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
        choices=ForPartyTypeChoices.choices, max_length=3, verbose_name="برای"
    )

    def __str__(self):
        return f"{self.for_who} | {self.category} | {self.title}"

    class Meta:
        verbose_name = "ویژگی مقداری"
        verbose_name_plural = "ویژگی های مقداری"


class CatalogMedicalCenter(Lookup):
    phone_number = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="شماره همراه"
    )

    class Meta:
        verbose_name = "مرکز همکار"
        verbose_name_plural = "مراکز همکار"


class WeekDay(Lookup):
    class Meta:
        verbose_name = "روز هفته"
        verbose_name_plural = "روز های هفته"
