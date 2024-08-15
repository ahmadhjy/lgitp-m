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

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # make sure that the periods are only created when we first
        # start making the activity not on save
        if not change:
            self.create_periods(obj)

    def create_periods(self, activity):
        offers = ActivityOffer.objects.filter(activity=activity)
        for offer in offers:
            # this can be changed to current date in case the available_from
            # date has passed
            current_date = offer.activity.available_from

            # creating date for calculating differences in date i guess
            # make sure the time of the activity do not pass one day since we
            # are making periods based on one day divided by period duration
            delta = timedelta(days=1)
            period_duration = timedelta(minutes=offer.activity.period)

            activity_start_time = offer.activity.start_time
            activity_end_time = offer.activity.end_time

            # also available_from should always be before the available_to
            while current_date <= offer.activity.available_to:
                period_start_time = datetime.combine(current_date, activity_start_time)
                period_end_time = period_start_time + period_duration

                # make sure that the period from to is correct
                # so that start_time is always before end time
                while period_end_time.time() <= activity_end_time:
                    Period.objects.create(
                        day=current_date,
                        time_from=period_start_time.time(),
                        time_to=period_end_time.time(),
                        stock=offer.stock,
                        activity_offer=offer,
                    )
                    # everytime a period is created its end time
                    # is the start time of the next one
                    period_start_time = period_end_time
                    period_end_time = period_start_time + period_duration
                # jump to the next day
                current_date += delta


admin.site.register(Period)
