from django.core.management.base import BaseCommand

from korrupsiya_app.telegram import _get_telegram_credentials, set_telegram_webhook


class Command(BaseCommand):
    help = "Register Telegram bot webhook for inline button callbacks"

    def add_arguments(self, parser):
        parser.add_argument(
            "webhook_url",
            nargs="?",
            default="https://korrupsiya.kuprikqurilish.uz/api/telegram/webhook/",
            help="Public HTTPS webhook URL",
        )

    def handle(self, *args, **options):
        token, _ = _get_telegram_credentials()
        if not token:
            self.stderr.write(self.style.ERROR("Telegram bot token topilmadi"))
            return

        webhook_url = options["webhook_url"]
        ok, message = set_telegram_webhook(webhook_url)
        if ok:
            self.stdout.write(self.style.SUCCESS(f"{message}: {webhook_url}"))
        else:
            self.stderr.write(self.style.ERROR(message))
