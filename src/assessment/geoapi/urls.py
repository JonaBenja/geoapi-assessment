from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import GeoLocationList


urlpatterns = [
    path("locations/", GeoLocationList.as_view(), name="location-list"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
