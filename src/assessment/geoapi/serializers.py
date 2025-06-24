from rest_framework import serializers
from .models import GeoLocation


class GeoLocationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = GeoLocation
        fields = ["location", "timestamp", "user"]
