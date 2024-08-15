from .models import Location
from .serializers import LocationSerializer
from rest_framework.decorators import (
        api_view,
        permission_classes
        )
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def get_locations(request):
    locations = Location.objects.all()
    serializer = LocationSerializer(locations, many=True)
    return Response(serializer.data)
