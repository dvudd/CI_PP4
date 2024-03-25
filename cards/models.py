from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from PIL import Image
from io import BytesIO
import os


# Create your models here.
class Subject(models.Model):
    """
    Represents a subject under which decks of flashcards can be categorized.

    Attributes:
        name (str): The name of the subject.
        creator (User): The user who created the subject.
        created_at (datetime): The date and time when the subject was created.
    """
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Deck(models.Model):
    """
    Represents a deck of cards within a subject.

    Attributes:
        name (str): The name of the deck.
        description (str): A description of the deck.
        subject (Subject): The subject to which the deck belongs.
        created_at (datetime): The date and time when the deck was created.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


def card_img(instance, filename):
    """
    Determines the path where the card image will be stored.

    Arguments:
        instance (Card): The card instance.
        filename (str): The original filename of the uploaded image.

    Returns:
        str: The path where the card image will be stored.
    """
    return 'user_{0}/{1}'.format(
        instance.deck.subject.creator.username,
        filename
    )


class Card(models.Model):
    """
    Represents a flashcard within a deck.

    Attributes:
        question (str): The question or front side of the card.
        question_image (ImageField): The image for the question side.
        answer (str): The answer or back side of the card.
        answer_image (ImageField): The image for the answer side.
        deck (Deck): The deck to which the card belongs.
        created_at (datetime): The date and time when the card was created.
    """
    question = models.TextField(blank=True)
    question_image = models.ImageField(
        upload_to=card_img,
        blank=True,
        null=True
    )
    answer = models.TextField(blank=True)
    answer_image = models.ImageField(
        upload_to=card_img,
        blank=True,
        null=True
    )
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def clean(self):
        """
        Validates that either text or image is provided for both the
        question and the answer.
        """
        if not self.question and not self.question_image:
            raise ValidationError(
                'You must provide either a question or an image.'
            )
        if not self.answer and not self.answer_image:
            raise ValidationError(
                'You must provide either a answer or an image.'
            )

    def save(self, *args, **kwargs):
        """
        Overridden save method to process images before saving.
        """
        self.clean()
        # Process question image
        if self.question_image:
            self.process_image(self.question_image)

        # Process answer image
        if self.answer_image:
            self.process_image(self.answer_image)

        super().save(*args, **kwargs)

    def process_image(self, image_field):
        """
        Processes the image by resizing and converting it to WEBP format.

        Arguments:
            image_field (ImageField): The image field to process.
        """
        MAX_SIZE = (800, 800)
        with Image.open(image_field) as img:
            # Resize the image if it's bigger than 800px
            img.thumbnail(MAX_SIZE)

            # Create a BytesIO object to save the image
            in_mem_file = BytesIO()
            img.save(in_mem_file, format='WEBP')
            in_mem_file.seek(0)

            # Change the file extension to .webp
            filename = os.path.basename(image_field.name)
            image_field.save(
                filename,
                ContentFile(in_mem_file.read()),
                save=False
            )
