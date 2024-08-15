from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from knox.views import (
    LogoutView as KnoxLogoutView,
    LogoutAllView as KnoxLogoutAllView
)
from .serializers import (UserSerializer, RegisterSerializer,
                          CustomerSerializer, SupplierSerializer,
                          UpdateEmailSerializer, UpdatePasswordSerializer,
                          UpdateSupplierLocationSerializer, UpdateCustomerLocationsSerializer,
                          UpdateCustomerPreferencesSerializer, UpdatePhoneSerializer)
from .models import Customer, Supplier
from rest_framework import status
from location.models import Location
from categories.models import Category


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_customer_preferences_api(request):
    user = request.user
    if not user.is_customer:
        return Response({"error": "Only customers can update their preferences."}, status=status.HTTP_403_FORBIDDEN)
    try:
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        return Response({"error": "Customer profile not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = UpdateCustomerPreferencesSerializer(customer, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Preferences updated successfully"})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_customer_locations_api(request):
    user = request.user
    if not user.is_customer:
        return Response({"error": "Only customers can update their locations."}, status=status.HTTP_403_FORBIDDEN)
    try:
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        return Response({"error": "Customer profile not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = UpdateCustomerLocationsSerializer(customer, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Locations updated successfully"})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_supplier_location_api(request):
    user = request.user
    if not user.is_supplier:
        return Response(
            {"error": "Only suppliers can update their location."},
            status=status.HTTP_403_FORBIDDEN)
    try:
        supplier = Supplier.objects.get(user=user)
    except Supplier.DoesNotExist:
        return Response(
            {"error": "Supplier profile not found."},
            status=status.HTTP_404_NOT_FOUND)
    serializer = UpdateSupplierLocationSerializer(supplier, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Supplier location updated successfully"})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_phone_api(request):
    user = request.user
    serializer = UpdatePhoneSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Phone number updated successfully"})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_email_api(request):
    user = request.user
    serializer = UpdateEmailSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Email updated successfully"})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_password_api(request):
    serializer = UpdatePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Password updated successfully"})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_api(request):
    user = request.user
    userserializer = UserSerializer(user)
    if user.is_customer:
        customer = Customer.objects.get(user=user)
        profileserializer = CustomerSerializer(customer)
    elif user.is_supplier:
        supplier = Supplier.objects.get(user=user)
        profileserializer = SupplierSerializer(supplier)
    data = {
        "user": userserializer.data,
        "profile": profileserializer.data
    }
    return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = AuthToken.objects.create(user)[1]
    if serializer.is_valid():
        Customer.objects.create(user=user)
        Customer.preferences = Category.objects.all()
        Customer.location = Location.objects.all()
    return Response({
        "user": UserSerializer(user, context={'request': request}).data,
        "token": token
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    login(request, user)
    token = AuthToken.objects.create(user)[1]
    return Response({
        "user": UserSerializer(user, context={'request': request}).data,
        "token": token
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_api(request):
    return KnoxLogoutView.as_view()(request._request)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_all_api(request):
    return KnoxLogoutAllView.as_view()(request._request)
