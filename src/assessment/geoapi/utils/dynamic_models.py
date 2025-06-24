from assessment.geoapi.models import GeoLocationBase
from django.contrib.gis.db import models
from rest_framework import serializers, viewsets
from assessment.urls import dynamic_router

FIELD_MAP = {
    "CharField": models.CharField,
    "DateTimeField": models.DateTimeField,
    "IntegerField": models.IntegerField,
    "PointField": models.PointField,
}


def register_dynamic_model(name, fields, original_config):
    attrs = {
        "__module__": "geoapi.models",
        "Meta": type("Meta", (), {"app_label": "geoapi"}),
    }

    for field_name, field_type in fields.items():
        field_class = FIELD_MAP[field_type]
        kwargs = {"max_length": 255} if field_type == "CharField" else {}
        attrs[field_name] = field_class(**kwargs)

    attrs["config"] = models.JSONField(default=original_config)

    model_class = type(name, (GeoLocationBase,), attrs)

    class Meta:
        model = model_class
        fields = "__all__"

    serializer_class = type(
        f"{name}Serializer", (serializers.ModelSerializer,), {"Meta": Meta}
    )

    viewset_class = type(
        f"{name}ViewSet",
        (viewsets.ModelViewSet,),
        {"queryset": model_class.objects.all(), "serializer_class": serializer_class},
    )
    basename = name.lower() + "s"
    dynamic_router.register(basename, viewset_class, basename=basename)

    print(f"Registering model: {name}")
    print(f"URL prefix: {name.lower()}s")
    print(f"Fields: {fields}")
    print("Registered viewset:", viewset_class.__name__)
