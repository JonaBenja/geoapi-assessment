from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .filters import GeoLocationFilter
from .models import GeoLocation
from .serializers import GeoLocationSerializer, ModelConfigUploadSerializer
from .utils.dynamic_models import register_dynamic_model


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


class AddConfigView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ModelConfigUploadSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data["name"]
            fields = serializer.validated_data["fields"]

            try:
                # Register model and attach the config as a field
                register_dynamic_model(
                    name, fields, original_config={"name": name, "fields": fields}
                )

                return Response(
                    {"message": f"Dynamisch model '{name}' aangemaakt."},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response(
                    {
                        "message": f"Fout bij het aanmaken van het model '{name}'.",
                        "error": str(e),
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
