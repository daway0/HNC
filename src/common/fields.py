from django.db import models


class ToomanField(models.PositiveBigIntegerField):

    def __init__(self, *args, **kwargs):
        kwargs["help_text"] = "قیمت به تومان است"
        super().__init__(*args, **kwargs)
