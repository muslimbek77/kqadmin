import re
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from korrupsiya_app.models import KarrupsiyaMalumot, KorrupsiyaFile

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}
FILE_EXTENSIONS = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".zip", ".rar"}
SKIP_DIRS = {"murojaatlar"}
MIN_FILE_SIZE = 100


def generate_title(filename: str) -> str:
    stem = Path(filename).stem
    stem = re.sub(r"_[A-Za-z0-9]{5,8}$", "", stem)
    stem = stem.replace("_", " ").replace("-", " ")
    stem = re.sub(r"\s+", " ", stem).strip()
    if not stem:
        return Path(filename).name
    return stem[0].upper() + stem[1:]


def is_thumbnail(path: Path) -> bool:
    return path.stem.endswith("_thumb")


def iter_media_files(media_root: Path, subdir: str, extensions: set):
    folder = media_root / subdir
    if not folder.exists():
        return
    for path in sorted(folder.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in extensions:
            continue
        if is_thumbnail(path):
            continue
        if path.stat().st_size < MIN_FILE_SIZE:
            continue
        yield path.relative_to(media_root).as_posix()


class Command(BaseCommand):
    help = "Restore existing media files into KarrupsiyaMalumot and KorrupsiyaFile records"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be created without writing to the database",
        )

    def handle(self, *args, **options):
        media_root = Path(settings.MEDIA_ROOT)
        dry_run = options["dry_run"]

        existing_images = {
            obj.image.name
            for obj in KarrupsiyaMalumot.objects.exclude(image="")
            if obj.image
        }
        existing_files = {
            obj.file.name
            for obj in KorrupsiyaFile.objects.exclude(file="")
            if obj.file
        }

        created_malumot = 0
        created_file = 0
        skipped = 0

        image_paths = set()
        for subdir in ("korrupsiya_images", "uploads"):
            if subdir in SKIP_DIRS:
                continue
            for rel_path in iter_media_files(media_root, subdir, IMAGE_EXTENSIONS):
                image_paths.add(rel_path)

        for rel_path in sorted(image_paths):
            if rel_path in existing_images:
                skipped += 1
                continue

            title = generate_title(Path(rel_path).name)
            if dry_run:
                self.stdout.write(f"[dry-run] KarrupsiyaMalumot: {title!r} <- {rel_path}")
                created_malumot += 1
                continue

            obj = KarrupsiyaMalumot(title=title, text="<p></p>")
            obj.image.name = rel_path
            obj.save()
            created_malumot += 1
            self.stdout.write(self.style.SUCCESS(f"KarrupsiyaMalumot: {title!r} <- {rel_path}"))

        for rel_path in iter_media_files(media_root, "korrupsiya_files", FILE_EXTENSIONS):
            if rel_path in existing_files:
                skipped += 1
                continue

            title = generate_title(Path(rel_path).name)
            if dry_run:
                self.stdout.write(f"[dry-run] KorrupsiyaFile: {title!r} <- {rel_path}")
                created_file += 1
                continue

            obj = KorrupsiyaFile(title=title)
            obj.file.name = rel_path
            obj.save()
            created_file += 1
            self.stdout.write(self.style.SUCCESS(f"KorrupsiyaFile: {title!r} <- {rel_path}"))

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Done. KarrupsiyaMalumot: {created_malumot}, "
                f"KorrupsiyaFile: {created_file}, skipped: {skipped}"
            )
        )
