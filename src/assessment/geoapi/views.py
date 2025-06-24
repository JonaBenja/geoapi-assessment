from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .filters import GeoLocationFilter
from .models import GeoLocation
from .serializers import GeoLocationSerializer


class GeoLocationListView(generics.ListAPIView):

    serializer_class = GeoLocationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = GeoLocationFilter

    def get_queryset(self):
        return GeoLocation.objects.filter(user=self.request.user)


class GeoLocationCreateView(generics.CreateAPIView):
    serializer_class = GeoLocationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GeoLocation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
