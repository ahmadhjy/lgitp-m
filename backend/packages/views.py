from .models import Package, PackageDay, PackageOffer
from .serializers import PackageSerializer, PackageDaySerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils import timezone


@api_view(["GET"])
@permission_classes([AllowAny])
def get_packages(request):
    current_time = timezone.now()
    packages = Package.objects.filter(available_to__gte=current_time)[:20]
    serializer = PackageSerializer(packages, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_packages(request):
    current_time = timezone.now()
    packages = Package.objects.filter(available_to__gte=current_time)
    serializer = PackageSerializer(packages, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_package(request, pk):
    package = Package.objects.get(pk=pk)
    serializer = PackageSerializer(package)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_package_days(request, package_offer_id):
    try:
        package_offer = PackageOffer.objects.get(pk=package_offer_id)
        package_days = PackageDay.objects.filter(package_offer=package_offer)
        serializer = PackageDaySerializer(package_days, many=True)
        return Response(serializer.data)
    except PackageOffer.DoesNotExist:
        return Response(
            {"error": "Package offer not found."}, status=status.HTTP_404_NOT_FOUND
        )
