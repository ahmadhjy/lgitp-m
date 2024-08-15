from rest_framework.serializers import ModelSerializer
from .models import ActivityBooking, PackageBooking, TourBooking
from activities.serializers import PeriodSerializer
from packages.serializers import PackageSerializer, PackageOfferSerializer
from tours.serializers import TourDaySerializer
from users.serializers import CustomerSerializer


class ActivityBookingSerializer(ModelSerializer):
    customer = CustomerSerializer()
    period = PeriodSerializer()

    class Meta:
        model = ActivityBooking
        fields = "__all__"


class PackageBookingSerializer(ModelSerializer):
    package_offer = PackageOfferSerializer()
    customer = CustomerSerializer()

    class Meta:
        model = PackageBooking
        fields = [
            "id",
            "package_offer",
            "customer",
            "start_date",
            "end_date",
            "confirmed",
            "paid",
            "quantity",
            "created_at",
            "qr_code",
        ]
        read_only_fields = [
            "id",
            "customer",
            "confirmed",
            "paid",
            "created_at",
            "qr_code",
        ]


class TourBookingSerializer(ModelSerializer):
    tourday = TourDaySerializer()
    customer = CustomerSerializer()

    class Meta:
        model = TourBooking
        fields = "__all__"
