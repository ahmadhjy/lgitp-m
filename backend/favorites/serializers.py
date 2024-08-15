from rest_framework import serializers
from .models import FavoriteActivity, FavoriteTour, FavoritePackage
from activities.serializers import ActivitySerializer
from tours.serializers import TourSerializer
from packages.serializers import PackageSerializer


class FavoriteActivitySerializer(serializers.ModelSerializer):
    activity = ActivitySerializer(read_only=True)

    class Meta:
        model = FavoriteActivity
        fields = ['activity']


class FavoriteTourSerializer(serializers.ModelSerializer):
    tour = TourSerializer(read_only=True)

    class Meta:
        model = FavoriteTour
        fields = ['tour']


class FavoritePackageSerializer(serializers.ModelSerializer):
    package = PackageSerializer(read_only=True)

    class Meta:
        model = FavoritePackage
        fields = ['package']
