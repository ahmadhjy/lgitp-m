from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from activities.models import Activity
from activities.serializers import ActivitySerializer
from tours.models import Tour
from tours.serializers import TourSerializer
from packages.models import Package
from packages.serializers import PackageSerializer
from users.models import Customer
from django.db.models import Q
from django.utils import timezone


@api_view(["GET"])
@permission_classes([AllowAny])
def for_you_items(request):
    customer = Customer.objects.get(user=request.user)
    preferred_locations = customer.location.all()
    preferred_categories = customer.preferences.all()

    current_time = timezone.now()
    activities = Activity.objects.filter(
        location__in=preferred_locations,
        categories__in=preferred_categories,
        available_to__gte=current_time,
    ).distinct()
    packages = Package.objects.filter(
        location__in=preferred_locations,
        categories__in=preferred_categories,
        available_to__gte=current_time,
    ).distinct()
    tours = Tour.objects.filter(
        location__in=preferred_locations,
        categories__in=preferred_categories,
        available_to__gte=current_time,
    ).distinct()

    activity_serializer = ActivitySerializer(activities, many=True)
    package_serializer = PackageSerializer(packages, many=True)
    tour_serializer = TourSerializer(tours, many=True)

    combined_results = {
        "activities": activity_serializer.data,
        "packages": package_serializer.data,
        "tours": tour_serializer.data,
    }

    return Response(combined_results)


@api_view(["GET"])
@permission_classes([AllowAny])
def latest_items_api(request):
    current_time = timezone.now()
    activities = Activity.objects.filter(
        available_to__gte=current_time,
    ).order_by(
        "-created_at"
    )[:4]
    tours = Tour.objects.filter(
        available_to__gte=current_time,
    ).order_by(
        "-created_at"
    )[:3]
    packages = Package.objects.filter(
        available_to__gte=current_time,
    ).order_by(
        "-created_at"
    )[:3]
    activity_serializer = ActivitySerializer(activities, many=True)
    tour_serializer = TourSerializer(tours, many=True)
    package_serializer = PackageSerializer(packages, many=True)
    data = {
        "activities": activity_serializer.data,
        "tours": tour_serializer.data,
        "packages": package_serializer.data,
    }
    return Response(data)


@api_view(["GET"])
@permission_classes([AllowAny])
def featured_items_api(request):
    # Fetch featured items from each model
    current_time = timezone.now()
    activities = Activity.objects.filter(
        featured=True,
        available_to__gte=current_time,
    ).order_by("-created_at")[:10]
    tours = Tour.objects.filter(
        featured=True,
        available_to__gte=current_time,
    ).order_by("-created_at")[:10]
    packages = Package.objects.filter(
        featured=True,
        available_to__gte=current_time,
    ).order_by("-created_at")[:10]
    activity_serializer = ActivitySerializer(activities, many=True)
    tour_serializer = TourSerializer(tours, many=True)
    package_serializer = PackageSerializer(packages, many=True)
    data = {
        "activities": activity_serializer.data,
        "tours": tour_serializer.data,
        "packages": package_serializer.data,
    }
    return Response(data)


@api_view(["GET"])
@permission_classes([AllowAny])
def search(request):
    query = request.GET.get("query", "")

    if query:
        activity_results = Activity.objects.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(location__name__icontains=query)
        )
        tour_results = Tour.objects.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(location__name__icontains=query)
        )
        package_results = Package.objects.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(location__name__icontains=query)
        )
    else:
        activity_results = Activity.objects.none()
        tour_results = Tour.objects.none()
        package_results = Package.objects.none()

    activity_serializer = ActivitySerializer(activity_results, many=True)
    tour_serializer = TourSerializer(tour_results, many=True)
    package_serializer = PackageSerializer(package_results, many=True)

    return Response(
        {
            "activities": activity_serializer.data,
            "tours": tour_serializer.data,
            "packages": package_serializer.data,
        },
        status=status.HTTP_200_OK,
    )
