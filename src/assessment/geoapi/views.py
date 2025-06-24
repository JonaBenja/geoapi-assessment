from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics

from .models import GeoLocation
from .serializers import GeoLocationSerializer


class GeoLocationList(generics.ListCreateAPIView):
    queryset = GeoLocation.objects.all()
    serializer_class = GeoLocationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
