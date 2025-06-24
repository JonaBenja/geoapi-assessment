from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import GeoLocationListView, GeoLocationCreateView


urlpatterns = [
    path("locations/", GeoLocationListView.as_view(), name="location-list"),
    path("locations/add/", GeoLocationCreateView.as_view(), name="location-create"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
