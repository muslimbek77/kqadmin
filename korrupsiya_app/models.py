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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Malumot for {self.title}"

class KorrupsiyaFile(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='korrupsiya_files/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title