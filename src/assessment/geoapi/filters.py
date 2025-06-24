from django import forms
import django_filters
from django_filters import rest_framework as filters
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSException
from .models import GeoLocation


class GeoLocationFilter(django_filters.FilterSet):
    reference_id = filters.ModelChoiceFilter(
        method="filter_by_reference_point",
        queryset=GeoLocation.objects.none(),
        label="Referentiepunt",
        to_field_name="pk",
        widget=forms.Select(),
    )

    radius = django_filters.NumberFilter(
        method="filter_by_reference_point", field_name="radius", label="Straal (meters)"
    )

    class Meta:
        model = GeoLocation
        fields = []

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super().__init__(data, queryset, request=request, prefix=prefix)
        self.request = request
        if self.request and self.request.user.is_authenticated:
            self.filters["reference_id"].queryset = GeoLocation.objects.filter(
                user=self.request.user
            )

    def filter_by_reference_point(self, queryset, name, value):
        try:
            reference_id = int(self.data.get("reference_id"))
            radius = int(self.data.get("radius"))
            ref_instance = GeoLocation.objects.get(pk=reference_id)
            ref_point = ref_instance.location
        except (TypeError, ValueError, GeoLocation.DoesNotExist, GEOSException):
            return queryset

        return (
            queryset.exclude(pk=ref_instance.pk)
            .filter(location__distance_lte=(ref_point, radius))
            .annotate(distance=Distance("location", ref_point))
            .order_by("distance")
        )
