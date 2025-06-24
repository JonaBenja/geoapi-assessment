from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from urllib.parse import urlencode

from .factories import GeoLocationFactory
from .models import GeoLocation


User = get_user_model()


class GeoLocationAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):

        # Create 3 different test users
        cls.user_1 = User.objects.create_user(
            username="user_1", password="secret123", email="test@example.com"
        )

        cls.user_2 = User.objects.create_user(
            username="user_2", password="secret123", email="test@example.com"
        )

        cls.user_3 = User.objects.create_user(
            username="user_3", password="secret123", email="test@example.com"
        )

        # For each user, create a GeoLocation instance
        cls.geo_1 = GeoLocationFactory(user=cls.user_1)
        cls.geo_2 = GeoLocationFactory(user=cls.user_2)
        cls.geo_3 = GeoLocationFactory(user=cls.user_3)

    def test_list_locations(self):
        url = reverse("location-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)

    def test_create_location_unauthenticated(self):
        url = reverse("location-list")
        data = {"latitude": "52.354868", "longitude": "4.896128"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_location_authenticated(self):
        self.client.force_authenticate(user=self.user_1)
        url = reverse("location-list")
        data = {"latitude": "52.354868", "longitude": "4.896128"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_location_invalid_latitude(self):
        self.client.force_authenticate(user=self.user_1)
        url = reverse("location-list")
        data = {"latitude": "102.354868", "longitude": "4.896128"}
        response = self.client.post(url, data)
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_location_invalid_longitude(self):
        self.client.force_authenticate(user=self.user_1)
        url = reverse("location-list")
        data = {"latitude": "52.354868", "longitude": "-200.896128"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
