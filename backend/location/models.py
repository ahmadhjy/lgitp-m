from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "locations"

    def __str__(self):
        return self.name
