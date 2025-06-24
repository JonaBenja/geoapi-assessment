import random

from django.contrib.gis.geos import Point
import factory

from .models import GeoLocation


class GeoLocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GeoLocation

    location = factory.LazyFunction(
        lambda: Point(
            4.896128 + random.uniform(-0.01, 0.01),
            52.354868 + random.uniform(-0.01, 0.01),
        )
    )
