from django.db import models
from django.contrib.auth import get_user_model
from activities.models import Activity
from tours.models import Tour
from packages.models import Package


User = get_user_model()


class FavoriteActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'activity')


class FavoriteTour(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'tour')


class FavoritePackage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'package')
