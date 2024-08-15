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

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # directly generate tour days on save for each offer
            if not obj.days_off:
                obj.days_off = ""
            days_off = [day.strip().lower() for day in obj.days_off.split(",")]
            current_day = obj.available_from
            offers = TourOffer.objects.filter(tour=obj)
            while current_day <= obj.available_to:
                if current_day.strftime("%A").lower() not in days_off:
                    for offer in offers:
                        TourDay.objects.get_or_create(
                            day=current_day,
                            tour_offer=offer,
                            defaults={"stock": offer.stock},
                        )
                current_day += timedelta(days=1)


admin.site.register(Tour, TourAdmin)
admin.site.register(TourDay)
