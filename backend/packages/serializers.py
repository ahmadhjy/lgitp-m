from rest_framework import serializers
from .models import (
    Package,
    PackageDay,
    Included,
    Excluded,
    Faq,
    Catalog,
    ItineraryStep,
    PackageOffer,
)
from location.serializers import LocationSerializer


class IncludedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Included
        fields = ["id", "include"]


class ExcludedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Excluded
        fields = ["id", "Exclude"]


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = ["id", "question", "answer"]


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = ["id", "image"]


class ItineraryStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryStep
        fields = "__all__"


class OffPackageSerializer(serializers.ModelSerializer):
    included_items = IncludedSerializer(
        many=True, read_only=True, source="included_set"
    )
    excluded_items = ExcludedSerializer(
        many=True, read_only=True, source="excluded_set"
    )
    faqs = FaqSerializer(many=True, read_only=True, source="faq_set")
    catalogs = CatalogSerializer(many=True, read_only=True, source="catalog_set")
    location = LocationSerializer()
    itinerary = ItineraryStepSerializer(
        many=True, read_only=True, source="itinerary_step_set"
    )

    class Meta:
        model = Package
        fields = "__all__"


class PackageOfferSerializer(serializers.ModelSerializer):
    package = OffPackageSerializer()

    class Meta:
        model = PackageOffer
        fields = ["id", "title", "price", "stock", "package"]


class PackageSerializer(serializers.ModelSerializer):
    included_items = IncludedSerializer(
        many=True, read_only=True, source="included_set"
    )
    excluded_items = ExcludedSerializer(
        many=True, read_only=True, source="excluded_set"
    )
    faqs = FaqSerializer(many=True, read_only=True, source="faq_set")
    catalogs = CatalogSerializer(many=True, read_only=True, source="catalog_set")
    location = LocationSerializer()
    itinerary = ItineraryStepSerializer(
        many=True, read_only=True, source="itinerary_step_set"
    )
    offers = PackageOfferSerializer(many=True, read_only=True)

    class Meta:
        model = Package
        fields = "__all__"


class PackageDaySerializer(serializers.ModelSerializer):
    package_offer = PackageOfferSerializer()

    class Meta:
        model = PackageDay
        fields = "__all__"
