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

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # If the package is being created
            if not obj.days_off:
                obj.days_off = ""
            days_off = [day.strip().lower() for day in obj.days_off.split(",")]
            current_day = obj.available_from
            offers = PackageOffer.objects.filter(package=obj)
            while current_day <= obj.available_to:
                if current_day.strftime("%A").lower() not in days_off:
                    for offer in offers:
                        PackageDay.objects.create(
                            day=current_day,
                            package_offer=offer,
                            stock=offer.stock,
                        )
                current_day += timedelta(days=1)


admin.site.register(Package, PackageAdmin)
admin.site.register(PackageDay)
