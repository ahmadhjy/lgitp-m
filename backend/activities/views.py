from .models import Activity, Period, ActivityOffer
from .serializers import ActivitySerializer, PeriodSerializer, ActivityOfferSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone


@api_view(["GET"])
@permission_classes([AllowAny])
def get_offers_by_activity(request, activity_id):
    try:
        activity = Activity.objects.get(pk=activity_id)
    except Activity.DoesNotExist:
        return Response(
            {"error": "Activity not found"}, status=status.HTTP_404_NOT_FOUND
        )

    offers = ActivityOffer.objects.filter(activity=activity)
    serializer = ActivityOfferSerializer(offers, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_activities(request):
    # timezone of the server, should be set to Lebanon
    current_time = timezone.now()
    # exclude items that their time has passed
    activities = Activity.objects.filter(available_to__gte=current_time)
    serializer = ActivitySerializer(activities, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_activity(request, pk):
    activity = Activity.objects.get(pk=pk)
    serializer = ActivitySerializer(activity)
    return Response(serializer.data)


# main page activities, exclude passed and only 20 ordered
@api_view(["GET"])
@permission_classes([AllowAny])
def get_activities(request):
    current_time = timezone.now()
    activities = Activity.objects.filter(available_to__gte=current_time)[:20]
    serializer = ActivitySerializer(activities, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_periods_by_offer_and_day(request, offer_id, day):
    try:
        offer = ActivityOffer.objects.get(pk=offer_id)
    except ActivityOffer.DoesNotExist:
        return Response({"error": "Offer not found"}, status=status.HTTP_404_NOT_FOUND)

    periods = Period.objects.filter(activity_offer=offer, day=day, stock__gt=0)
    serializer = PeriodSerializer(periods, many=True)
    return Response(serializer.data)
