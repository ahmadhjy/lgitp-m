from rest_framework import serializers
from .models import (
    Tour,
    TourDay,
    Included,
    Excluded,
    Faq,
    Catalog,
    ItineraryStep,
    TourOffer,
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


class OffTourSerializer(serializers.ModelSerializer):
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
        many=True, read_only=True, source="itinerary_steps"
    )

    class Meta:
        model = Tour
        fields = "__all__"


class TourOfferSerializer(serializers.ModelSerializer):
    tour = OffTourSerializer()

    class Meta:
        model = TourOffer
        fields = ["id", "title", "price", "stock", "tour"]


class TourSerializer(serializers.ModelSerializer):
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
        many=True, read_only=True, source="itinerary_steps"
    )
    offers = TourOfferSerializer(many=True, read_only=True, source="tour_offer")

    class Meta:
        model = Tour
        fields = "__all__"


class TourDaySerializer(serializers.ModelSerializer):
    tour_offer = TourOfferSerializer()

    class Meta:
        model = TourDay
        fields = "__all__"
