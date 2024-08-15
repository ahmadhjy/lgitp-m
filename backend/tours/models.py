from django.db import models
from categories.models import Category
from users.models import Supplier
from location.models import Location
from datetime import timedelta

class Tour(models.Model):
    featured = models.BooleanField(default=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="tours/")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    available_from = models.DateField()
    available_to = models.DateField()
    categories = models.ManyToManyField(Category, related_name="tours", blank=True)
    stock = models.PositiveIntegerField(default=0)
    # one tour is always one day
    period = models.PositiveIntegerField(help_text="Period in hours")
    days_off = models.CharField(
        max_length=255, blank=True, null=True, help_text="Days off (comma-separated)"
    )
    unit = models.CharField(max_length=50)
    pickup_location = models.TextField()
    pickup_time = models.TimeField()
    dropoff_time = models.TimeField()
    languages = models.TextField(blank=True, null=True)
    min_age = models.IntegerField(blank=True, null=True)
    cancellation_policy = models.TextField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)

    def create_tour_days(self):
        if not self.days_off:
            self.days_off = ""
        days_off = [day.strip().lower() for day in self.days_off.split(",")]
        current_day = self.available_from
        offers = self.tour_offer.all()  # Use related name to access tour offers
        while current_day <= self.available_to:
            if current_day.strftime("%A").lower() not in days_off:
                for offer in offers:
                    TourDay.objects.get_or_create(
                        day=current_day,
                        tour_offer=offer,
                        defaults={"stock": offer.stock},
                    )
            current_day += timedelta(days=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "tours"


class TourOffer(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="tour_offer")
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.tour.title} - {self.title}"


class TourDay(models.Model):
    day = models.DateField()
    stock = models.IntegerField()
    tour_offer = models.ForeignKey(TourOffer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tour_offer.tour.title} - {self.day}"


class ItineraryStep(models.Model):

    tour = models.ForeignKey(
        Tour, related_name="itinerary_steps", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    activity = models.TextField(help_text="What to do there")

    def __str__(self):
        return f"{self.title} - {self.activity}"

    class Meta:
        verbose_name_plural = "Itinerary Steps"


class Included(models.Model):
    include = models.CharField(max_length=350)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)


class Excluded(models.Model):
    Exclude = models.CharField(max_length=350)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)


class Faq(models.Model):
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=500)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)


class Catalog(models.Model):
    image = models.ImageField(upload_to="activities/")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
