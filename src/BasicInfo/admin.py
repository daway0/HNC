from django.contrib import admin
from django.contrib.admin import ModelAdmin

from Equipments import models as eq_models

from . import models

admin.site.site_header = "مدیریت تهران درمان"
admin.site.site_title = "تهران درمان"
admin.site.index_title = "خوش آمدید"


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
        "display_path",
        "display_base_price",
        "display_healthcare_franchise",
        "display_personnel_franchise",
        "display_selectable",
    ]
    search_fields = ["title"]

    def get_search_results(self, request, queryset, search_term):
        r_qs, r_duplication = super().get_search_results(
            request, queryset, search_term
        )

        filtered_ids = [
            r_instance.id for r_instance in r_qs if r_instance.is_leaf
        ]
        return (
            r_qs.filter(id__in=filtered_ids),
            r_duplication,
        )

    @admin.display(description="دسته بندی")
    def display_path(self, obj):
        parent_path = obj.parent or "دسته بندی مادر"
        return str(parent_path)

    @admin.display(description="قیمت پایه سرویس")
    def display_base_price(self, obj):
        return obj.base_price if obj.is_leaf else ""

    @admin.display(description="سهم مرکز")
    def display_healthcare_franchise(self, obj):
        return f"{obj.healthcare_franchise}%" if obj.is_leaf else ""

    @admin.display(description="سهم پرسنل")
    def display_personnel_franchise(self, obj):
        return f"{100 - obj.healthcare_franchise}%" if obj.is_leaf else ""

    @admin.display(description="قابل انتخاب", boolean=True)
    def display_selectable(self, obj):
        return obj.is_leaf


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
