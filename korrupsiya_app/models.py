from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class Korrupsiya(models.Model):

    name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class KarrupsiyaMalumot(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='korrupsiya_images/', blank=True, null=True)
    text = RichTextUploadingField()
    seen_count = models.IntegerField(default=0, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Malumot for {self.title}"
    
    def increment_seen_count(self):
        self.seen_count += 1
        self.save(update_fields=['seen_count'])

class KorrupsiyaFile(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='korrupsiya_files/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    company = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    type = models.CharField(max_length=100, blank=True)
    work_hours = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=255, blank=True)

    salary = models.CharField(max_length=255, blank=True)
    experience = models.CharField(max_length=255, blank=True)
    education = models.CharField(max_length=255, blank=True)

    published_date = models.DateField()
    deadline = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=100)

    # Flexible fields using JSONField for lists
    responsibilities = models.JSONField(default=list, blank=True)
    requirements = models.JSONField(default=list, blank=True)
    languages = models.JSONField(default=list, blank=True)
    conditions = models.JSONField(default=list, blank=True)
    positions = models.JSONField(default=list, blank=True)

    # Extra flexible field for additional data
    extra = models.JSONField(default=dict, blank=True)

    # Multilingual support (choose one approach based on your needs)
    # Option 1: Separate fields
    # title_uz = models.CharField(max_length=255, blank=True)
    # title_ru = models.CharField(max_length=255, blank=True)
    # title_en = models.CharField(max_length=255, blank=True)

    # Option 2: JSONField with language keys
    title_translations = models.JSONField(default=dict, blank=True)  # {"uz": "", "ru": "", "en": ""}
    description_translations = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return f"{self.company} - {self.title}"