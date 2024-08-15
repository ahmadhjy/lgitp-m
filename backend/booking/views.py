from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from notifications.models import Notification
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from activities.models import Period
from tours.models import TourDay
from packages.models import PackageDay, PackageOffer
from users.models import Customer
from .models import ActivityBooking, TourBooking, PackageBooking
from .serializers import (
    ActivityBookingSerializer,
    TourBookingSerializer,
    PackageBookingSerializer,
)
from datetime import timedelta, datetime


@permission_classes([IsAuthenticated])
@api_view(["POST"])
def activity_booking_create(request):
    if not request.user.is_customer:
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        period_id = request.data.get("period_id")
        quantity = request.data.get("quantity")
        if not period_id:
            return Response(
                {"error": "Period is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        period = Period.objects.get(pk=period_id)
        customer = Customer.objects.get(user=request.user)

        if period.stock < 1:
            return Response(
                {"error": "No available slots for this period."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        booking = ActivityBooking.objects.create(
            period=period, customer=customer, quantity=quantity
        )

        serializer = ActivityBookingSerializer(booking)
        Notification.objects.create(
            user=request.user,
            message=f"Booking {period.activity_offer.activity.title} created waiting for confirmation from {period.activity_offer.activity.supplier.user.username}",
        )
        Notification.objects.create(
            user=period.activity_offer.activity.supplier.user,
            message=f"Booking {period.activity_offer.activity.title} created waiting for your confirmation",
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Period.DoesNotExist:
        return Response(
            {"error": "Period not found."}, status=status.HTTP_404_NOT_FOUND
        )
    except Customer.DoesNotExist:
        return Response(
            {"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def tour_booking_create(request):
    customer = request.user.customer
    tourday_id = request.data.get("tourday_id")
    quantity = request.data.get("quantity", 1)

    if not tourday_id:
        return Response(
            {"error": "Tour day ID is required."}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        tourday = TourDay.objects.get(id=tourday_id)
    except TourDay.DoesNotExist:
        return Response(
            {"error": "Tour day not found."}, status=status.HTTP_404_NOT_FOUND
        )

    if tourday.stock < quantity:
        return Response(
            {
                "error": f"Not enough stock for this tour day. Available stock: {tourday.stock}"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    tourday.stock -= quantity
    tourday.save()

    booking = TourBooking(tourday=tourday, customer=customer, quantity=quantity)
    booking.save()

    serializer = TourBookingSerializer(booking)
    Notification.objects.create(
        user=request.user,
        message=f"Booking {tourday.tour_offer.title} created waiting for confirmation from {tourday.tour_offer.tour.supplier.user.username}",
    )
    Notification.objects.create(
        user=tourday.tour_offer.tour.supplier.user,
        message=f"New booking for {tourday.tour_offer.title} created waiting for your confirmation",
    )

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def package_booking_create(request):
    customer = request.user.customer
    package_offer_id = request.data.get("package_offer_id")
    if not package_offer_id:
        return Response(
            {"error": "Package offer ID is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        package_offer = PackageOffer.objects.get(id=package_offer_id)
    except PackageOffer.DoesNotExist:
        return Response(
            {"error": "Package offer not found."}, status=status.HTTP_404_NOT_FOUND
        )

    start_date = request.data.get("start_date")
    if not start_date:
        return Response(
            {"error": "Start date is required."}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    except ValueError:
        return Response(
            {"error": "Invalid date format. Use YYYY-MM-DD."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    quantity = request.data.get("quantity", 1)
    if quantity < 1:
        return Response(
            {"error": "Quantity must be at least 1."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    end_date = start_date + timedelta(days=package_offer.package.period - 1)
    if end_date > package_offer.package.available_to:
        return Response(
            {"error": "Package end date exceeds availability."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    package_days = PackageDay.objects.filter(
        package_offer=package_offer, day__range=(start_date, end_date)
    )
    if package_days.count() != package_offer.package.period:
        return Response(
            {"error": "Package days not fully available."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    for day in package_days:
        if day.stock < quantity:
            return Response(
                {
                    "error": f"Not enough stock for {day.day}. Available stock: {day.stock}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    for day in package_days:
        day.stock -= quantity
        day.save()

    booking = PackageBooking.objects.create(
        package_offer=package_offer,
        customer=customer,
        start_date=start_date,
        end_date=end_date,
        quantity=quantity,
    )

    serializer = PackageBookingSerializer(booking)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
