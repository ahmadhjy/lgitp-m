from django.contrib import admin
from .models import (
    Package,
    PackageDay,
    Included,
    Excluded,
    Faq,
    Catalog,
    ItineraryStep,
    PackageOffer,
)
from datetime import timedelta


class IncludedInline(admin.TabularInline):
    model = Included
    extra = 1


class ExcludedInline(admin.TabularInline):
    model = Excluded
    extra = 1


class FaqInline(admin.TabularInline):
    model = Faq
    extra = 1


class CatalogInline(admin.TabularInline):
    model = Catalog
    extra = 1


class ItineraryInline(admin.TabularInline):
    model = ItineraryStep
    extra = 1


class PackageOfferInline(admin.TabularInline):
    model = PackageOffer
    extra = 1


class PackageAdmin(admin.ModelAdmin):
    inlines = [
        PackageOfferInline,
        IncludedInline,
        ExcludedInline,
        FaqInline,
        CatalogInline,
        ItineraryInline,
    ]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if not change:
            form.instance.create_package_days()

admin.site.register(Package, PackageAdmin)
admin.site.register(PackageDay)
