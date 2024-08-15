from django.db import models
from users.models import Supplier
from categories.models import Category
from location.models import Location
from datetime import datetime, timedelta


class Activity(models.Model):
    featured = models.BooleanField(default=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="activities/")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    available_from = models.DateField()
    available_to = models.DateField()
    # map here is an html iframe from google maps
    map = models.TextField()
    categories = models.ManyToManyField(Category, related_name="activities", blank=True)
    # stock is no longer important in the model, but check where it's used
    # and change before deletion
    stock = models.PositiveIntegerField(default=0)
    period = models.PositiveIntegerField(help_text="Period in minutes")
    # comma separated days of the week
    days_off = models.CharField(
        max_length=255, blank=True, null=True, help_text="Days off (comma-separated)"
    )
    # TODO: unit here is no longer important
    unit = models.CharField(max_length=50)

    start_time = models.TimeField(help_text="Start time of the activity")
    end_time = models.TimeField(help_text="End time of the activity")

    # the model will be deleted if you delete the location where it is in.
    # is this right ?
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    audio_languages = models.TextField(blank=True, null=True)
    cancellation_policy = models.TextField(blank=True, null=True)
    group_size = models.CharField(max_length=50, blank=True, null=True)
    participant_age_range = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name_plural = "activities"

    def __str__(self):
        return self.title
    def create_periods(self):
        offers = self.offers.all()  # Use the related name to get the offers
        for offer in offers:
            current_date = self.available_from
            delta = timedelta(days=1)
            period_duration = timedelta(minutes=self.period)

            activity_start_time = self.start_time
            activity_end_time = self.end_time

            while current_date <= self.available_to:
                period_start_time = datetime.combine(current_date, activity_start_time)
                period_end_time = period_start_time + period_duration

                while period_end_time.time() <= activity_end_time:
                    Period.objects.create(
                        day=current_date,
                        time_from=period_start_time.time(),
                        time_to=period_end_time.time(),
                        stock=offer.stock,
                        activity_offer=offer,
                    )
                    period_start_time = period_end_time
                    period_end_time = period_start_time + period_duration
                current_date += delta


class ActivityOffer(models.Model):
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name="offers"
    )
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.activity.title} - {self.title}"


class Period(models.Model):
    day = models.DateField()
    time_from = models.TimeField()
    time_to = models.TimeField()
    stock = models.IntegerField()
    activity_offer = models.ForeignKey(
        ActivityOffer, on_delete=models.CASCADE, related_name="periods"
    )


class Included(models.Model):
    include = models.CharField(max_length=350)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)


class Excluded(models.Model):
    Exclude = models.CharField(max_length=350)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)


class Faq(models.Model):
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=500)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)


class Catalog(models.Model):
    image = models.ImageField(upload_to="activities/")
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
