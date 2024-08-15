from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from notifications.models import Notification
from booking.models import ActivityBooking, PackageBooking, TourBooking
from activities.models import Period, Activity
from packages.models import Package, PackageDay, PackageOffer
from tours.models import Tour, TourDay, TourOffer
from users.models import Supplier, Customer
from booking.serializers import (
    ActivityBookingSerializer,
    PackageBookingSerializer,
    TourBookingSerializer,
)
from datetime import timedelta, datetime


# Customer views for activity bookings
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def customer_activity_bookings(request):
    customer = get_object_or_404(Customer, user=request.user)
    bookings = ActivityBooking.objects.filter(customer=customer)
    serializer = ActivityBookingSerializer(bookings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Supplier views for activity bookings
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def supplier_activity_bookings(request):
    supplier = get_object_or_404(Supplier, user=request.user)
    activities = Activity.objects.filter(supplier=supplier)
    periods = Period.objects.filter(activity_offer__activity__in=activities)
    bookings = ActivityBooking.objects.filter(period__in=periods)
    serializer = ActivityBookingSerializer(bookings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def confirm_activity_booking(request, booking_id):
    supplier = get_object_or_404(Supplier, user=request.user)
    booking = get_object_or_404(ActivityBooking, id=booking_id)
    period = get_object_or_404(Period, pk=booking.period_id)
    if booking.period.activity_offer.activity.supplier != supplier:
        return Response(
            {"detail": "Not authorized to confirm this booking."},
            status=status.HTTP_403_FORBIDDEN,
        )

    booking.confirmed = True
    booking.generate_qr_code()
    period.stock -= booking.quantity
    period.save()
    booking.save()

    Notification.objects.create(
        user=booking.customer.user,
        message=f"Activity {period.activity_offer.activity.title} got confirmed",
    )
    serializer = ActivityBookingSerializer(booking)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def confirm_payment(request, booking_id):
    supplier = get_object_or_404(Supplier, user=request.user)
    booking = get_object_or_404(ActivityBooking, id=booking_id)
    if booking.period.activity_offer.activity.supplier != supplier:
        return Response(
            {"detail": "Not authorized to confirm payment for this booking."},
            status=status.HTTP_403_FORBIDDEN,
        )

    booking.paid = True
    booking.save()
    serializer = ActivityBookingSerializer(booking)

    Notification.objects.create(
        user=booking.customer.user, message="Activity Booking got paid"
    )
    Notification.objects.create(
        user=booking.period.activity_offer.activity.supplier.user,
        message="Activity Booking got paid",
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


# Customer views for package bookings
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def customer_package_bookings(request):
    customer = get_object_or_404(Customer, user=request.user)
    bookings = PackageBooking.objects.filter(customer=customer)
    serializer = PackageBookingSerializer(bookings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Supplier views for package bookings
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def supplier_packages_bookings(request):
    supplier = get_object_or_404(Supplier, user=request.user)
    packages = Package.objects.filter(supplier=supplier)
    bookings = PackageBooking.objects.filter(package_offer__package__in=packages)
    serializer = PackageBookingSerializer(bookings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def confirm_package_booking(request, booking_id):
    supplier = get_object_or_404(Supplier, user=request.user)
    booking = get_object_or_404(PackageBooking, id=booking_id)

    if booking.package_offer.package.supplier != supplier:
        return Response(
            {"detail": "Not authorized to confirm this booking."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if booking.confirmed:
        return Response(
            {"detail": "Booking is already confirmed."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    package = booking.package_offer.package
    start_date = booking.start_date
    end_date = start_date + timedelta(days=package.period - 1)
    package_days = PackageDay.objects.filter(
        package_offer=booking.package_offer, day__range=(start_date, end_date)
    )

    for day in package_days:
        if day.stock < 1:
            return Response(
                {"error": f"No available stock for {day.day}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    for day in package_days:
        day.stock -= booking.quantity
        day.save()

    booking.confirmed = True
    booking.generate_qr_code()
    booking.save()
    Notification.objects.create(
        user=booking.customer.user,
        message=f"Package {package.title} got confirmed, enjoy your time",
    )
    serializer = PackageBookingSerializer(booking)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def confirm_package_payment(request, booking_id):
    supplier = get_object_or_404(Supplier, user=request.user)
    booking = get_object_or_404(PackageBooking, id=booking_id)
    if booking.package_offer.package.supplier != supplier:
        return Response(
            {"detail": "Not authorized to confirm payment for this booking."},
            status=status.HTTP_403_FORBIDDEN,
        )

    booking.paid = True
    booking.save()
    serializer = PackageBookingSerializer(booking)

    Notification.objects.create(
        user=booking.customer.user, message="Package Booking got paid"
    )
    Notification.objects.create(
        user=booking.package_offer.package.supplier.user,
        message="Package Booking got paid",
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


# Customer views for tour bookings
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def customer_tour_bookings(request):
    customer = get_object_or_404(Customer, user=request.user)
    bookings = TourBooking.objects.filter(customer=customer)
    serializer = TourBookingSerializer(bookings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Supplier views for tour bookings
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def supplier_tours_bookings(request):
    supplier = get_object_or_404(Supplier, user=request.user)
    tours = Tour.objects.filter(supplier=supplier)
    days = TourDay.objects.filter(tour_offer__tour__in=tours)
    bookings = TourBooking.objects.filter(tourday__in=days)
    serializer = TourBookingSerializer(bookings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def confirm_tour_booking(request, booking_id):
    supplier = get_object_or_404(Supplier, user=request.user)
    booking = get_object_or_404(TourBooking, id=booking_id)
    if booking.tourday.tour_offer.tour.supplier != supplier:
        return Response(
            {"detail": "Not authorized to confirm this booking."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if booking.confirmed:
        return Response(
            {"detail": "Booking is already confirmed."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    tourday = booking.tourday
    if tourday.stock < 1:
        return Response(
            {"error": "No available stock for this tour day."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    tourday.stock -= booking.quantity
    tourday.save()

    booking.confirmed = True
    booking.generate_qr_code()
    booking.save()

    Notification.objects.create(
        user=booking.customer.user, message="Tour got confirmed, enjoy your time"
    )
    serializer = TourBookingSerializer(booking)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def confirm_tour_payment(request, booking_id):
    supplier = get_object_or_404(Supplier, user=request.user)
    booking = get_object_or_404(TourBooking, id=booking_id)
    if booking.tourday.tour_offer.tour.supplier != supplier:
        return Response(
            {"detail": "Not authorized to confirm payment for this booking."},
            status=status.HTTP_403_FORBIDDEN,
        )

    booking.paid = True
    booking.save()
    serializer = TourBookingSerializer(booking)
    Notification.objects.create(
        user=booking.customer.user, message="Tour Booking got paid"
    )
    Notification.objects.create(
        user=booking.tourday.tour_offer.tour.supplier.user,
        message="Tour Booking got paid",
    )
    return Response(serializer.data, status=status.HTTP_200_OK)
