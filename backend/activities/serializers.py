from rest_framework import serializers
from .models import Activity, Period, Included, Excluded, Faq, Catalog, ActivityOffer
from users.models import Supplier
from categories.models import Category
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


class OffActivitySerializer(serializers.ModelSerializer):
    included_items = IncludedSerializer(
        many=True, read_only=True, source="included_set"
    )
    excluded_items = ExcludedSerializer(
        many=True, read_only=True, source="excluded_set"
    )
    faqs = FaqSerializer(many=True, read_only=True, source="faq_set")
    catalogs = CatalogSerializer(many=True, read_only=True, source="catalog_set")
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True
    )
    location = LocationSerializer()

    class Meta:
        model = Activity
        fields = [
            "id",
            "supplier",
            "title",
            "image",
            "description",
            "price",
            "requests",
            "created_at",
            "available_from",
            "available_to",
            "categories",
            "stock",
            "period",
            "days_off",
            "unit",
            "start_time",
            "end_time",
            "location",
            "audio_languages",
            "cancellation_policy",
            "group_size",
            "participant_age_range",
            "included_items",
            "excluded_items",
            "faqs",
            "catalogs",
            "map",
        ]
        read_only_fields = ["created_at"]


class ActivityOfferSerializer(serializers.ModelSerializer):
    activity = OffActivitySerializer()

    class Meta:
        model = ActivityOffer
        fields = ["id", "title", "price", "stock", "activity"]


# here the fields are hardwritten one by one so in case we
# wanted to exclude something from the fields
class ActivitySerializer(serializers.ModelSerializer):
    included_items = IncludedSerializer(
        many=True, read_only=True, source="included_set"
    )
    excluded_items = ExcludedSerializer(
        many=True, read_only=True, source="excluded_set"
    )
    faqs = FaqSerializer(many=True, read_only=True, source="faq_set")
    catalogs = CatalogSerializer(many=True, read_only=True, source="catalog_set")
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True
    )
    location = LocationSerializer()
    offers = ActivityOfferSerializer(many=True, read_only=True)

    class Meta:
        model = Activity
        fields = [
            "id",
            "supplier",
            "title",
            "image",
            "description",
            "price",
            "requests",
            "created_at",
            "available_from",
            "available_to",
            "categories",
            "stock",
            "period",
            "days_off",
            "unit",
            "start_time",
            "end_time",
            "location",
            "audio_languages",
            "cancellation_policy",
            "group_size",
            "participant_age_range",
            "included_items",
            "excluded_items",
            "faqs",
            "catalogs",
            "map",
            "offers",
        ]
        read_only_fields = ["created_at"]


class PeriodSerializer(serializers.ModelSerializer):
    activity_offer = ActivityOfferSerializer()

    class Meta:
        model = Period
        fields = "__all__"
