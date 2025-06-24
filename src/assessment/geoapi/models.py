from django.contrib.gis.db import models
from django.contrib.auth import get_user_model


class GeoLocation(models.Model):
    location = models.PointField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.user or 'Mystery'} at {self.location}"


class GeoLocationBase(models.Model):
    location = models.PointField()
    timestamp = models.DateTimeField()

    class Meta:
        abstract = True
