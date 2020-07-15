import uuid
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

# Create your models here.


class Album(models.Model):
    title = models.CharField(max_length=70)
    thumb = ProcessedImageField(upload_to='albums', processors=[
                                ResizeToFit(300)], format='JPEG', options={'quality': 100})
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __unicode__(self):
        return self.title


class AlbumImage(models.Model):
    image = ProcessedImageField(upload_to='albums', processors=[
                                ResizeToFit(1200)], format='JPEG', options={'quality': 100})
    thumb = ProcessedImageField(upload_to='albums', processors=[
                                ResizeToFit(1200)], format='JPEG', options={'quality': 100})
    album = models.ForeignKey('album', on_delete=models.SET_NULL, null=True)
    alt = models.CharField(max_length=255, default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    slug = models.SlugField(
        max_length=70, default=uuid.uuid4, editable=False)
