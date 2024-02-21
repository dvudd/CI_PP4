from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import os

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    
class Deck(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

def card_img(instance, filename):
    return 'user_{0}/{1}'.format(instance.deck.subject.creator.username, filename)

class Card(models.Model):
    question = models.TextField()
    question_image = models.ImageField(upload_to=card_img, blank=True, null=True)
    answer = models.TextField()
    answer_image = models.ImageField(upload_to=card_img, blank=True, null=True)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Process question image
        if self.question_image:
            self.process_image(self.question_image)

        # Process answer image
        if self.answer_image:
            self.process_image(self.answer_image)

        super().save(*args, **kwargs)

    def process_image(self, image_field):
            MAX_SIZE = (800, 800)
            with Image.open(image_field) as img:
                # Resize the image if it's bigger than 300px
                img.thumbnail(MAX_SIZE)

                # Create a BytesIO object to save the image
                in_mem_file = BytesIO()
                img.save(in_mem_file, format='WEBP')
                in_mem_file.seek(0)

                # Change the file extension to .webp
                filename = os.path.basename(image_field.name)
                image_field.save(filename, ContentFile(in_mem_file.read()), save=False)