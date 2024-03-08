from django.db import models


class GenderChoices(models.TextChoices):
    MALE = "M", "مرد"
    FEMALE = "F", "زن"


class AreaChoices(models.TextChoices):
    # mantaqe1, mantaqe2, ...
    DISTRICT = "DIS", "منطقه"

    # pasdaran, iranshahr
    NEIGHBORHOOD = "NGB", "محله"

    # SHOMAL, JONUB, SHARQ, QARB
    AREA = "ARE", "محدوده"


class ForPartyTypeChoices(models.TextChoices):
    PERSONNEL = "PRS", "پرسنل"
    PATIENT = "PTN", "بیمار"
    CLIENT = "CLI", "کارفرما"
    COMMON = "CMN", "مشترک بین همه"


class CallTypeChoices(models.TextChoices):
    INCOMING = "INC", "ورودی"
    OUTGOING = "OUT", "خروجی"


class CallAnswerStatusChoices(models.TextChoices):
    ANSWERED = "ANS", "پاسخ داده شده"
    NOT_ANSWERED = "REJ", "رد شده"
