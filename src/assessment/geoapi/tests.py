from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point


from rest_framework.test import APITestCase
from rest_framework import status
from urllib.parse import urlencode

from .factories import GeoLocationFactory
from .models import GeoLocation


User = get_user_model()


class GeoLocationAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):

        # Create 2 different test users
        cls.user_1 = User.objects.create_user(
            username="user_1", password="secret123", email="test@example.com"
        )

        cls.user_2 = User.objects.create_user(
            username="user_2", password="secret123", email="test@example.com"
        )

        # Create GeoLocations with specific geospatial points for testing distance filter
        cls.geo_1 = GeoLocationFactory(
            user=cls.user_1, location=Point(4.896128, 52.354868)
        )

        # +/- 500m north of cls.geo_3, but different user
        cls.geo_2 = GeoLocationFactory(
            user=cls.user_2, location=Point(4.896128, 52.359368)
        )

        # +/- 500m north of cls.geo_3
        cls.geo_3 = GeoLocationFactory(
            user=cls.user_1, location=Point(4.896128, 52.359368)
        )

        # +/- 10.000m north of cls.geo_3
        cls.geo_4 = GeoLocationFactory(
            user=cls.user_1, location=Point(4.896128, 52.444968)
        )

    def test_list_locations_unauthenticated(self):
        url = reverse("location-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_locations_authenticated(self):
        self.client.force_authenticate(user=self.user_1)
        url = reverse("location-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_only_locations_created_by_user(self):
        url = reverse("location-list")

        # First get all locations for user 1
        self.client.force_authenticate(user=self.user_1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Make sure user 1 is the user of all locations
        results_user_1 = response.data["results"]
        self.assertTrue(all(item["user"] == "user_1" for item in results_user_1))

        # Then get all locations for user 2
        self.client.force_authenticate(user=self.user_2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Make sure user 2 is the user of all locations
        results_user_2 = response.data["results"]
        self.assertTrue(all(item["user"] == "user_2" for item in results_user_2))

        # Make sure locations of user 1 are different from locations of user 2
        self.assertNotEqual(results_user_1, results_user_2)

    def test_create_location_unauthenticated(self):
        url = reverse("location-create")
        data = {"latitude": "52.354868", "longitude": "4.896128"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_location_authenticated(self):
        self.client.force_authenticate(user=self.user_1)
        url = reverse("location-create")
        data = {"latitude": "52.354868", "longitude": "4.896128"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_location_invalid_latitude(self):
        self.client.force_authenticate(user=self.user_1)
        url = reverse("location-create")
        data = {"latitude": "102.354868", "longitude": "4.896128"}
        response = self.client.post(url, data)
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_location_invalid_longitude(self):
        self.client.force_authenticate(user=self.user_1)
        url = reverse("location-create")
        data = {"latitude": "52.354868", "longitude": "-200.896128"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_location_distance_1000_meters(self):
        self.client.force_authenticate(user=self.user_1)
        url = reverse("location-list")
        response = self.client.get(url, {"reference_id": 1, "radius": 1000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["id"], 3)
        self.assertEqual(response.data["results"][0]["user"], "user_1")

    def test_filter_location_distance_20000_meters(self):
        self.client.force_authenticate(user=self.user_1)
        url = reverse("location-list")
        response = self.client.get(url, {"reference_id": 1, "radius": 20000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_ids = {item["id"] for item in response.data["results"]}
        self.assertEqual(returned_ids, {3, 4})
        returned_users = {item["user"] for item in response.data["results"]}
        self.assertEqual(returned_users, {"user_1"})
