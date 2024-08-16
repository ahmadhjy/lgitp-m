from django.db import models
from users.models import Supplier
from categories.models import Category
from location.models import Location
from datetime import timedelta

class Package(models.Model):
    featured = models.BooleanField(default=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="packages/")
    description = models.TextField()
    duration = models.CharField(max_length=50)  # e.g., "8 hours"
    created_at = models.DateTimeField(auto_now_add=True)
    available_from = models.DateField()
    available_to = models.DateField()
    categories = models.ManyToManyField(Category, related_name="packages", blank=True)
    stock = models.PositiveIntegerField(default=0)
    period = models.PositiveIntegerField(help_text="Period in days")
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
    def create_package_days(self):
        if not self.days_off:
            self.days_off = ""
        days_off = [day.strip().lower() for day in self.days_off.split(",")]
        current_day = self.available_from
        offers = self.offers.all()  # Use related name to access package offers
        while current_day <= self.available_to:
            if current_day.strftime("%A").lower() not in days_off:
                for offer in offers:
                    PackageDay.objects.create(
                        day=current_day,
                        package_offer=offer,
                        stock=offer.stock,
                    )
            current_day += timedelta(days=1)

    def __str__(self):
        return self.title


class PackageOffer(models.Model):
    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, related_name="offers"
    )
    title = models.CharField(max_length=255)  # e.g., "Standard", "Deluxe"
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.package.title} - {self.title}"


class PackageDay(models.Model):
    day = models.DateField()
    package_offer = models.ForeignKey(PackageOffer, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.package_offer.package.title} - {self.day}"


class ItineraryStep(models.Model):
    package = models.ForeignKey(
        Package, related_name="itinerary_step_set", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    activity = models.TextField(help_text="What to do there")

    def __str__(self):
        return f"{self.title} - {self.activity}"

    class Meta:
        verbose_name_plural = "Itinerary Steps"


class Included(models.Model):
    include = models.CharField(max_length=350)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)


class Excluded(models.Model):
    Exclude = models.CharField(max_length=350)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)


class Faq(models.Model):
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=500)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)


class Catalog(models.Model):
    image = models.ImageField(upload_to="activities/")
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
