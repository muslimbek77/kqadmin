import json
import logging
import mimetypes
import os
import urllib.error
import urllib.request
from uuid import uuid4

from django.conf import settings

from .models import Murojaat, TelegramSettings

logger = logging.getLogger(__name__)


def _build_message(murojaat):
    lines = [
        "Yangi murojaat qabul qilindi:",
        f"ID: {murojaat.pk}",
        f"Tel: {murojaat.phone_number}",
        f"Manzil: {murojaat.address}",
        f"Status: {murojaat.get_status_display()}",
        f"Mazmun: {murojaat.content}",
    ]
    return "\n".join(lines)


def _get_telegram_credentials():
    telegram_settings = TelegramSettings.load()
    token = telegram_settings.bot_token or getattr(settings, "TELEGRAM_BOT_TOKEN", "")
    chat_id = telegram_settings.admin_chat_id or getattr(settings, "TELEGRAM_DEFAULT_CHAT_ID", "")
    return token, chat_id


def _build_status_keyboard(murojaat):
    statuses = [
        (Murojaat.Status.TUSHUNTIRILDI, "Tushuntirildi"),
        (Murojaat.Status.QONIQTIRILDI, "Qoniqtirildi"),
        (Murojaat.Status.RAD_ETILDI, "Rad etildi"),
    ]
    buttons = []
    for status_code, label in statuses:
        prefix = "✅ " if murojaat.status == status_code else ""
        buttons.append(
            {
                "text": f"{prefix}{label}",
                "callback_data": f"murojaat_status:{murojaat.pk}:{status_code}",
            }
        )
    return {"inline_keyboard": [buttons]}


def _create_multipart_body(fields, files):
    boundary = f"----WebKitFormBoundary{uuid4().hex}"
    body = bytearray()

    for name, value in fields.items():
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"))
        body.extend(str(value).encode("utf-8"))
        body.extend(b"\r\n")

    for name, file_info in files.items():
        filename, content, content_type = file_info
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(
            (
                f'Content-Disposition: form-data; name="{name}"; '
                f'filename="{os.path.basename(filename)}"\r\n'
            ).encode("utf-8")
        )
        body.extend(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
        body.extend(content)
        body.extend(b"\r\n")

    body.extend(f"--{boundary}--\r\n".encode("utf-8"))
    return bytes(body), boundary


def _send_telegram_request(token, method, payload=None, files=None):
    payload = payload or {}
    files = files or {}
    url = f"https://api.telegram.org/bot{token}/{method}"

    if files:
        body, boundary = _create_multipart_body(payload, files)
        headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"}
        request = urllib.request.Request(url=url, data=body, headers=headers, method="POST")
    else:
        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            url=url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

    with urllib.request.urlopen(request, timeout=10) as response:
        response_body = response.read()

    if not response_body:
        return {}
    return json.loads(response_body.decode("utf-8"))


def send_murojaat_to_telegram(murojaat):
    token, chat_id = _get_telegram_credentials()
    if not token or not chat_id:
        logger.warning("Telegram token yoki chat_id topilmadi")
        return False

    message = _build_message(murojaat)

    try:
        if murojaat.attachment:
            content_type = mimetypes.guess_type(murojaat.attachment.name)[0] or "application/octet-stream"
            with murojaat.attachment.open("rb") as attachment_file:
                result = _send_telegram_request(
                    token=token,
                    method="sendDocument",
                    payload={
                        "chat_id": chat_id,
                        "caption": message[:1024],
                    },
                    files={
                        "document": (
                            murojaat.attachment.name,
                            attachment_file.read(),
                            content_type,
                        )
                    },
                )
                logger.info(f"Telegram document yuborildi: {result}")
        else:
            result = _send_telegram_request(
                token=token,
                method="sendMessage",
                payload={
                    "chat_id": chat_id,
                    "text": message,
                },
            )
            logger.info(f"Telegram message yuborildi: {result}")
    except Exception as e:
        logger.exception(f"Failed to send murojaat {murojaat.pk} to Telegram: {str(e)}")
        return False

    return True


def handle_telegram_callback(callback_query):
    token, _ = _get_telegram_credentials()
    if not token:
        return False

    data = callback_query.get("data", "")
    prefix = "murojaat_status:"
    if not data.startswith(prefix):
        return False

    try:
        _, murojaat_id, status = data.split(":")
        murojaat = Murojaat.objects.get(pk=int(murojaat_id))
        if status not in Murojaat.Status.values:
            return False
    except (Murojaat.DoesNotExist, TypeError, ValueError):
        return False

    murojaat.status = status
    murojaat.save(update_fields=["status", "updated_at"])

    message = callback_query.get("message", {})
    chat = message.get("chat", {})
    message_id = message.get("message_id")
    chat_id = chat.get("id")
    callback_query_id = callback_query.get("id")

    try:
        _send_telegram_request(
            token=token,
            method="answerCallbackQuery",
            payload={
                "callback_query_id": callback_query_id,
                "text": f"Status: {murojaat.get_status_display()}",
            },
        )
    except Exception:
        logger.exception(
            "Failed to answer Telegram callback for murojaat %s", murojaat.pk
        )

    if chat_id and message_id:
        try:
            _send_telegram_request(
                token=token,
                method="editMessageReplyMarkup",
                payload={
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "reply_markup": _build_status_keyboard(murojaat),
                },
            )
        except Exception:
            logger.exception(
                "Failed to update Telegram keyboard for murojaat %s", murojaat.pk
            )

    return True


def set_telegram_webhook(webhook_url):
    token, _ = _get_telegram_credentials()
    if not token:
        return False, "Telegram bot token topilmadi"

    try:
        response = _send_telegram_request(
            token=token,
            method="setWebhook",
            payload={
                "url": webhook_url,
                "allowed_updates": ["callback_query"],
            },
        )
    except Exception as exc:
        logger.exception("Failed to set Telegram webhook")
        return False, str(exc)

    if not response.get("ok"):
        return False, response.get("description", "Webhook o'rnatilmadi")

    return True, response.get("description", "Webhook o'rnatildi")
