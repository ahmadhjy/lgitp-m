from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from activities.models import Activity
from tours.models import Tour
from packages.models import Package
from .models import FavoriteActivity, FavoriteTour, FavoritePackage
from django.contrib.auth import get_user_model
from .serializers import FavoriteActivitySerializer, FavoriteTourSerializer, FavoritePackageSerializer

User = get_user_model()


@api_view(['GET'])
def all_favorites(request):
    user = request.user

    favorite_activities = FavoriteActivity.objects.filter(user=user)
    favorite_tours = FavoriteTour.objects.filter(user=user)
    favorite_packages = FavoritePackage.objects.filter(user=user)

    activity_serializer = FavoriteActivitySerializer(favorite_activities, many=True)
    tour_serializer = FavoriteTourSerializer(favorite_tours, many=True)
    package_serializer = FavoritePackageSerializer(favorite_packages, many=True)

    combined_favorites = {
        'activities': activity_serializer.data,
        'tours': tour_serializer.data,
        'packages': package_serializer.data
    }

    return Response(combined_favorites, status=status.HTTP_200_OK)


# Add or remove favorite activity, and check if it's a favorite
@api_view(['POST', 'DELETE', 'GET'])
def favorite_activity(request, activity_id):
    user = request.user
    activity = get_object_or_404(Activity, id=activity_id)

    if request.method == 'POST':
        favorite, created = FavoriteActivity.objects.get_or_create(user=user, activity=activity)
        if created:
            return Response({'status': 'Activity added to favorites'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'Activity already in favorites'}, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        favorite = get_object_or_404(FavoriteActivity, user=user, activity=activity)
        favorite.delete()
        return Response({'status': 'Activity removed from favorites'}, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'GET':
        is_favorite = FavoriteActivity.objects.filter(user=user, activity=activity).exists()
        return Response({'is_favorite': is_favorite}, status=status.HTTP_200_OK)


# Add or remove favorite tour, and check if it's a favorite
@api_view(['POST', 'DELETE', 'GET'])
def favorite_tour(request, tour_id):
    user = request.user
    tour = get_object_or_404(Tour, id=tour_id)

    if request.method == 'POST':
        favorite, created = FavoriteTour.objects.get_or_create(user=user, tour=tour)
        if created:
            return Response({'status': 'Tour added to favorites'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'Tour already in favorites'}, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        favorite = get_object_or_404(FavoriteTour, user=user, tour=tour)
        favorite.delete()
        return Response({'status': 'Tour removed from favorites'}, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'GET':
        is_favorite = FavoriteTour.objects.filter(user=user, tour=tour).exists()
        return Response({'is_favorite': is_favorite}, status=status.HTTP_200_OK)


# Add or remove favorite package, and check if it's a favorite
@api_view(['POST', 'DELETE', 'GET'])
def favorite_package(request, package_id):
    user = request.user
    package = get_object_or_404(Package, id=package_id)

    if request.method == 'POST':
        favorite, created = FavoritePackage.objects.get_or_create(user=user, package=package)
        if created:
            return Response({'status': 'Package added to favorites'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'Package already in favorites'}, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        favorite = get_object_or_404(FavoritePackage, user=user, package=package)
        favorite.delete()
        return Response({'status': 'Package removed from favorites'}, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'GET':
        is_favorite = FavoritePackage.objects.filter(user=user, package=package).exists()
        return Response({'is_favorite': is_favorite}, status=status.HTTP_200_OK)
