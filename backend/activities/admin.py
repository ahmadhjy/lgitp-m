from django.contrib import admin
from datetime import datetime, timedelta
from .models import Activity, Period, Included, Excluded, Faq, Catalog, ActivityOffer

# inlines are used to make adding one to many relationship on the
# same page in the admin panel


class ActivityOfferInline(admin.TabularInline):
    model = ActivityOffer
    extra = 1


class PeriodInline(admin.TabularInline):
    model = Period
    extra = 1


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


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "supplier", "available_from", "available_to")
    list_filter = ("supplier", "categories", "available_from", "available_to")
    search_fields = ("title", "description", "supplier__name")
    inlines = [
        ActivityOfferInline,
        IncludedInline,
        ExcludedInline,
        FaqInline,
        CatalogInline,
    ]
    filter_horizontal = ("categories",)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        # At this point, all the related objects (ActivityOffers) are saved
        if not change:  # If the activity is being created
            form.instance.create_periods()


admin.site.register(Period)
