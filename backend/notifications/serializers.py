from rest_framework import serializers
from .models import Notification


# here the serializer is for display the create will be only
# from the signal and from the booking create function (make
# sure to handle error and that the mode is saved before
# creating the Notification because this might cause errors)
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
