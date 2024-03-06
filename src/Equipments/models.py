from BasicInfo.models import Lookup
from django.db import models


class CatalogEquipment(Lookup):
    current_price = models.IntegerField(default=0, verbose_name="قیمت فعلی")

    class Meta:
        verbose_name = "تجهیز"
        verbose_name_plural = "تجهیزات"
