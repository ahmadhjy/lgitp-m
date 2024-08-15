from django.db import models
from django.contrib.auth.models import AbstractUser
from location.models import Location
from categories.models import Category


class CustomUser(AbstractUser):
    is_supplier = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    phone = models.CharField(max_length=15)


class Supplier(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL,
                                 null=True, blank=True)

    def __str__(self):
        return self.user.username


class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    location = models.ManyToManyField(Location, blank=True)
    preferences = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.user.username
