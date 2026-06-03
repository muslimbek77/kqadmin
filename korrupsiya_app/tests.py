from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Murojaat


class MurojaatAPITests(APITestCase):
    @patch("korrupsiya_app.views.send_murojaat_to_telegram")
    def test_create_murojaat_with_attachment(self, mocked_send):
        mocked_send.return_value = True
        payload = {
            "phone_number": "+998901234567",
            "address": "Toshkent shahri",
            "content": "Sinov murojaati",
            "attachment": SimpleUploadedFile("test.txt", b"hello", content_type="text/plain"),
        }

        response = self.client.post(reverse("murojaat-list-create"), payload, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Murojaat.objects.count(), 1)
        self.assertEqual(Murojaat.objects.first().status, Murojaat.Status.NEW)
        mocked_send.assert_called_once()

    def test_update_murojaat_status(self):
        murojaat = Murojaat.objects.create(
            phone_number="+998901112233",
            address="Samarqand",
            content="Statusni yangilash testi",
        )

        response = self.client.patch(
            reverse("murojaat-status-update", kwargs={"pk": murojaat.pk}),
            {"status": Murojaat.Status.QONIQTIRILDI},
            format="json",
        )

        murojaat.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(murojaat.status, Murojaat.Status.QONIQTIRILDI)

    def test_murojaat_statistics(self):
        Murojaat.objects.create(
            phone_number="+998900000001",
            address="Andijon",
            content="1",
            status=Murojaat.Status.TUSHUNTIRILDI,
        )
        Murojaat.objects.create(
            phone_number="+998900000002",
            address="Namangan",
            content="2",
            status=Murojaat.Status.RAD_ETILDI,
            telegram_error="failed",
        )
        Murojaat.objects.create(
            phone_number="+998900000003",
            address="Farg'ona",
            content="3",
            status=Murojaat.Status.QONIQTIRILDI,
        )

        response = self.client.get(reverse("murojaat-statistics"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total"], 3)
        self.assertEqual(response.data["tushuntirildi"], 1)
        self.assertEqual(response.data["qoniqtirildi"], 1)
        self.assertEqual(response.data["rad_etildi"], 1)
        self.assertEqual(response.data["telegram_failed"], 1)
