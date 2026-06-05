import json
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Murojaat, TelegramSettings
from .telegram import handle_telegram_callback, send_murojaat_to_telegram


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


class TelegramIntegrationTests(APITestCase):
    @patch("korrupsiya_app.telegram.urllib.request.urlopen")
    def test_send_murojaat_with_file_uses_send_document(self, mocked_urlopen):
        mocked_urlopen.return_value.__enter__.return_value.read.return_value = b'{"ok": true, "result": {}}'
        TelegramSettings.objects.update_or_create(
            pk=1,
            defaults={"bot_token": "panel-token", "admin_chat_id": "7605884028"},
        )
        murojaat = Murojaat.objects.create(
            phone_number="+998901234567",
            address="Toshkent",
            content="Admin panel sozlamasi testi",
            attachment=SimpleUploadedFile(
                "individual_loyiha.pdf",
                b"%PDF-1.4 test",
                content_type="application/pdf",
            ),
        )

        result = send_murojaat_to_telegram(murojaat)

        self.assertTrue(result)
        request = mocked_urlopen.call_args.args[0]
        self.assertEqual(request.full_url, "https://api.telegram.org/botpanel-token/sendDocument")

    @override_settings(TELEGRAM_BOT_TOKEN="env-token", TELEGRAM_DEFAULT_CHAT_ID="777")
    @patch("korrupsiya_app.telegram.urllib.request.urlopen")
    def test_send_murojaat_without_file_uses_send_message(self, mocked_urlopen):
        mocked_urlopen.return_value.__enter__.return_value.read.return_value = b'{"ok": true, "result": {}}'
        murojaat = Murojaat.objects.create(
            phone_number="+998901234568",
            address="Buxoro",
            content="Env fallback testi",
        )

        result = send_murojaat_to_telegram(murojaat)

        self.assertTrue(result)
        request = mocked_urlopen.call_args.args[0]
        self.assertEqual(request.full_url, "https://api.telegram.org/botenv-token/sendMessage")
        payload = json.loads(request.data.decode("utf-8"))
        self.assertIn("reply_markup", payload)

    @patch("korrupsiya_app.telegram._send_telegram_request")
    def test_callback_updates_murojaat_status(self, mocked_request):
        TelegramSettings.objects.update_or_create(
            pk=1,
            defaults={"bot_token": "panel-token", "admin_chat_id": "7605884028"},
        )
        murojaat = Murojaat.objects.create(
            phone_number="+998901234569",
            address="Xiva",
            content="Callback testi",
        )

        result = handle_telegram_callback(
            {
                "id": "callback-id",
                "data": f"murojaat_status:{murojaat.pk}:{Murojaat.Status.QONIQTIRILDI}",
                "message": {"message_id": 15, "chat": {"id": 7605884028}},
            }
        )

        murojaat.refresh_from_db()
        self.assertTrue(result)
        self.assertEqual(murojaat.status, Murojaat.Status.QONIQTIRILDI)
        self.assertEqual(mocked_request.call_count, 2)

    @patch("korrupsiya_app.views.handle_telegram_callback")
    def test_telegram_webhook_endpoint(self, mocked_callback):
        mocked_callback.return_value = True

        response = self.client.post(
            reverse("telegram-webhook"),
            {
                "callback_query": {
                    "id": "callback-id",
                    "data": "murojaat_status:1:qoniqtirildi",
                    "message": {"message_id": 15, "chat": {"id": 7605884028}},
                }
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"ok": True})
