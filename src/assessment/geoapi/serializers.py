from django.contrib.gis.geos import Point

from rest_framework import serializers

from .models import GeoLocation


class GeoLocationSerializer(serializers.ModelSerializer):
    """
    Serializer for the GeoLocation model.

    Allows creation of GeoLocation points from latitude and longitude inputs.
    Includes validation of the latitude and longitude inputs.
    Creates a Point() object from latitude and longitude.
    """

    user = serializers.StringRelatedField(read_only=True)
    latitude = serializers.FloatField(
        write_only=True,
        help_text="Latitude in graden (°)",
        initial=52.3702,
    )

    longitude = serializers.FloatField(
        write_only=True,
        help_text="Longitude in graden (°)",
        initial=4.8948,
    )

    class Meta:
        model = GeoLocation
        fields = ["id", "latitude", "longitude", "location", "timestamp", "user"]
        read_only_fields = ["location", "timestamp", "user"]

    def validate(self, data):
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if not (-90 <= latitude <= 90):
            raise serializers.ValidationError(
                "Latitude needs to be between -90 and 90."
            )
        if not (-180 <= longitude <= 180):
            raise serializers.ValidationError(
                "Longitude needs to be between -180 and 180."
            )

        return data

    def create(self, validated_data):
        longitude = validated_data.pop("longitude")
        latitude = validated_data.pop("latitude")
        point = Point(longitude, latitude)
        return GeoLocation.objects.create(location=point, **validated_data)


ALLOWED_FIELD_TYPES = {"CharField", "DateTimeField", "IntegerField", "PointField"}


class ModelConfigUploadSerializer(serializers.Serializer):
    name = serializers.CharField()
    fields = serializers.DictField(child=serializers.CharField())

    def validate_fields(self, fields):
        for field_name, field_type in fields.items():
            if field_type not in ALLOWED_FIELD_TYPES:
                raise serializers.ValidationError(
                    f"Unsupported field type: {field_type}"
                )
        return fields
