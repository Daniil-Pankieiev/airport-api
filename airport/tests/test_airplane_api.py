import tempfile
import os

from PIL import Image
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from .samples import sample_airplane, sample_airplane_type
from ..models import Airplane
from ..serializers import AirplaneListSerializer


FLIGHT_URL = reverse("airport:flight-list")
AIRPLANE_URL = reverse("airport:airplane-list")


def remove_tickets_available(data):
    for instance in data:
        instance.pop("tickets_available")


def flight_detail_url(flight_id):
    return reverse("airport:flight-detail", args=[flight_id])


def image_upload_url(airplane_id):
    """Return URL for recipe image upload"""
    return reverse("airport:airplane-upload-image", args=[airplane_id])


def detail_url(airplane_id):
    return reverse("airport:airplane-detail", args=[airplane_id])


class AirplaneImageUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.airplane_type = sample_airplane_type(name="Airplanetype2")
        self.airplane = sample_airplane()

    def tearDown(self):
        self.airplane.image.delete()

    def test_upload_image_to_airplane(self):
        """Test uploading an image to airplame"""
        url = image_upload_url(self.airplane.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(url, {"image": ntf}, format="multipart")
        self.airplane.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("image", res.data)
        self.assertTrue(os.path.exists(self.airplane.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image"""
        url = image_upload_url(self.airplane.id)
        res = self.client.post(url, {"image": "not image"}, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_image_to_airplane_list(self):
        url = AIRPLANE_URL
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(
                url,
                {
                    "name": "Sampleairplane1",
                    "rows": 19,
                    "seats_in_row": 7,
                    "airplane_type": self.airplane_type.id,
                    "image": ntf,
                },
                format="multipart",
            )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_image_url_is_shown_on_airplane_list(self):
        url = image_upload_url(self.airplane.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            self.client.post(url, {"image": ntf}, format="multipart")
        res = self.client.get(AIRPLANE_URL)

        self.assertIn("image", res.data[0].keys())


class UnAuthenticatedAirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        result = self.client.get(AIRPLANE_URL)
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)

    def test_list_airplanes(self):
        sample_airplane()
        result = self.client.get(AIRPLANE_URL)
        airplanes = Airplane.objects.all()
        serializer = AirplaneListSerializer(airplanes, many=True)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_create_airplane_forbidden(self):
        payload = {
            "name": "Sampleairplane",
            "rows": 19,
            "seats_in_row": 7,
            "airplane_type": sample_airplane_type(),
        }
        result = self.client.post(AIRPLANE_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirplaneApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)

    def test_create_airplane(self):
        airplane_type = sample_airplane_type()
        payload = {
            "name": "Sampleairplane",
            "rows": 19,
            "seats_in_row": 7,
            "airplane_type": airplane_type.id,
        }
        response = self.client.post(AIRPLANE_URL, payload)

        airplane = Airplane.objects.get(id=response.data["id"])

        airplane_type_airplane = airplane.airplane_type
        del payload["airplane_type"]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(airplane_type_airplane, airplane_type)
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(airplane, key))
