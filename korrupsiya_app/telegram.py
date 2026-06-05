import json
import urllib.error
import urllib.request

from django.conf import settings
from django.utils import timezone

from .models import TelegramSettings


def _build_message(murojaat):
    lines = [
        "Yangi murojaat qabul qilindi:",
        f"ID: {murojaat.pk}",
        f"Tel: {murojaat.phone_number}",
        f"Manzil: {murojaat.address}",
        f"Status: {murojaat.get_status_display()}",
        f"Mazmun: {murojaat.content}",
    ]
    if murojaat.attachment:
        lines.append(f"Fayl: {murojaat.attachment.url}")
    return "\n".join(lines)


def _get_telegram_credentials():
    telegram_settings = TelegramSettings.load()
    token = telegram_settings.bot_token or getattr(settings, "TELEGRAM_BOT_TOKEN", "")
    default_chat_id = telegram_settings.admin_chat_id or getattr(
        settings, "TELEGRAM_DEFAULT_CHAT_ID", ""
    )
    return token, default_chat_id


def send_murojaat_to_telegram(murojaat):
    token, default_chat_id = _get_telegram_credentials()
    chat_id = murojaat.assigned_telegram_chat_id or default_chat_id

    if not token or not chat_id:
        murojaat.telegram_error = "Telegram token yoki chat id sozlanmagan."
        murojaat.save(update_fields=["telegram_error", "updated_at"])
        return False

    payload = json.dumps(
        {
            "chat_id": chat_id,
            "text": _build_message(murojaat),
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        url=f"https://api.telegram.org/bot{token}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            response.read()
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
        murojaat.telegram_error = str(exc)
        murojaat.save(update_fields=["telegram_error", "updated_at"])
        return False

    murojaat.telegram_sent_at = timezone.now()
    murojaat.telegram_error = ""
    murojaat.save(update_fields=["telegram_sent_at", "telegram_error", "updated_at"])
    return True
