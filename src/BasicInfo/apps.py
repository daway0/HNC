from typing import Any
from django.apps import AppConfig


class BasicinfoConfig(AppConfig):
    def __init__(self, app_name: str, app_module: Any | None) -> None:
        super().__init__(app_name, app_module)
        self.icon = "Home"

    default_auto_field = "django.db.models.BigAutoField"
    name = "BasicInfo"
    verbose_name = "اطلاعات پایه"

