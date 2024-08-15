from .models import Tour, TourDay, TourOffer
from .serializers import TourSerializer, TourDaySerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.utils import timezone


@api_view(["GET"])
@permission_classes([AllowAny])
def get_tours(request):
    current_time = timezone.now()
    packages = Tour.objects.filter(available_to__gte=current_time)[:20]
    serializer = TourSerializer(packages, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_tours(request):
    current_time = timezone.now()
    packages = Tour.objects.filter(available_to__gte=current_time)
    serializer = TourSerializer(packages, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_tour(request, pk):
    package = Tour.objects.get(pk=pk)
    serializer = TourSerializer(package)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_tour_days(request, tour_offer_id):
    try:
        tour_offer = TourOffer.objects.get(pk=tour_offer_id)
        tour_days = TourDay.objects.filter(tour_offer=tour_offer)
        serializer = TourDaySerializer(tour_days, many=True)
        return Response(serializer.data)
    except TourOffer.DoesNotExist:
        return Response(
            {"error": "Tour offer not found."}, status=status.HTTP_404_NOT_FOUND
        )
