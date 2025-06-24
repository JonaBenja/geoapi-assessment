from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from .models import GeoLocation
from .serializers import GeoLocationSerializer


class GeoLocationList(generics.ListCreateAPIView):
    queryset = GeoLocation.objects.all()
    serializer_class = GeoLocationSerializer
    permission_classes = [IsAuthenticated]

    # Save user that created the instance
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Only return locations created by current user
    def get_queryset(self):
        return GeoLocation.objects.filter(user=self.request.user)
