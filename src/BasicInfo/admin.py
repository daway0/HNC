from django.contrib import admin
from django.contrib.admin import ModelAdmin
from Equipments import models as eq_models

from . import models


@admin.register(
    eq_models.CatalogEquipment,
    models.CatalogMedicalCenter,
    models.CatalogPersonnelRole,
    models.CatalogTagSpecificationCategory,
    models.CatalogValuedSpecificationCategory,
    models.CatalogCallReferral,
    models.CatalogCallReason,
    models.WeekDay,
)
class CatalogAdmin(ModelAdmin):
    list_display = [
        "title",
    ]
    search_fields = ["title"]


@admin.register(models.CatalogService)
class CatalogServiceAdmin(ModelAdmin):
    list_display = [
        "title",
        "base_price",
        "display_healthcare_franchise",
        "display_personnel_franchise",
    ]
    search_fields = ["title"]

    @admin.display(description="سهم مرکز")
    def display_healthcare_franchise(self, obj):
        return f"{obj.healthcare_franchise}%"

    @admin.display(description="سهم پرسنل")
    def display_personnel_franchise(self, obj):
        return f"{100 - obj.healthcare_franchise}%"


@admin.register(
    models.CatalogTagSpecification,
    models.CatalogValuedSpecification,
)
class CatalogWithCategoryAdmin(ModelAdmin):
    list_display = ["title", "category"]
    search_fields = ["title"]


@admin.register(models.CatalogArea)
class CatalogAreaAdmin(ModelAdmin):
    list_display = ["title", "category"]
    search_fields = ["title"]
    list_filter = ["category"]
