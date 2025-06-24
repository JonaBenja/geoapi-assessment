from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    path("", views.GeoLocationListView.as_view(), name="location-list"),
    path("add/", views.GeoLocationCreateView.as_view(), name="location-create"),
    path("add_config/", views.AddConfigView.as_view(), name="add_config"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
