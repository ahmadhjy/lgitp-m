from django.contrib import admin
from .models import (
    Tour,
    TourDay,
    Included,
    Excluded,
    Faq,
    Catalog,
    ItineraryStep,
    TourOffer,
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


class TourOfferInline(admin.TabularInline):
    model = TourOffer
    extra = 1


class TourAdmin(admin.ModelAdmin):
    inlines = [
        TourOfferInline,
        IncludedInline,
        ExcludedInline,
        FaqInline,
        CatalogInline,
        ItineraryInline,
    ]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if not change:
            form.instance.create_tour_days()



admin.site.register(Tour, TourAdmin)
admin.site.register(TourDay)
