from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Customer, Supplier
from location.serializers import LocationSerializer
from location.models import Location
from categories.serializers import CategorySerializer
from categories.models import Category

User = get_user_model()


class UpdateCustomerPreferencesSerializer(serializers.ModelSerializer):
    preferences = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)

    class Meta:
        model = Customer
        fields = ['preferences']

    def update(self, instance, validated_data):
        instance.preferences.set(validated_data['preferences'])
        instance.save()
        return instance


class UpdateCustomerLocationsSerializer(serializers.ModelSerializer):
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), many=True)

    class Meta:
        model = Customer
        fields = ['location']

    def update(self, instance, validated_data):
        instance.location.set(validated_data['location'])
        instance.save()
        return instance


class UpdateSupplierLocationSerializer(serializers.ModelSerializer):
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())

    class Meta:
        model = Supplier
        fields = ['location']

    def update(self, instance, validated_data):
        instance.location = validated_data['location']
        instance.save()
        return instance


class UpdateEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

    def update(self, instance, validated_data):
        instance.email = validated_data['email']
        instance.save()
        return instance

class UpdatePhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone']

    def update(self, instance, validated_data):
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance

class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value

    def validate_new_password(self, value):
        # Add any custom validation for the new password here
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class SupplierSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Supplier
        fields = ('id', 'location')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone', 'username', 'email', 'is_supplier', 'is_customer')


class CustomerSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=True)
    preferences = CategorySerializer(many=True)
    user = UserSerializer()
    class Meta:
        model = Customer
        fields = ('id', 'location', 'preferences', 'user')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'phone')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data['phone'],
            is_customer=True
        )
        return user
