import os
from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Subject, Deck, Card
from PIL import Image

class ModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.subject = Subject.objects.create(name="Nostalgia", creator=cls.user)
        cls.deck = Deck.objects.create(name="Cartoons", subject=cls.subject)
        cls.large_image_path = os.path.join(settings.BASE_DIR, 'cards/tests/test_images/sample-large.jpg')
        cls.small_image_path = os.path.join(settings.BASE_DIR, 'cards/tests/test_images/sample-small.jpg')

    def test_subject_creation(self):
        self.assertEqual(self.subject.name, "Nostalgia")
        self.assertEqual(self.subject.creator.username, "testuser")

    def test_deck_creation(self):
        deck = Deck.objects.get(id=1)
        self.assertEqual(deck.name, "Cartoons")
        self.assertEqual(deck.subject.name, "Nostalgia")

    def test_card_creation_with_question(self):
        deck = Deck.objects.get(id=1)
        card = Card(question="Who lives in a pineapple under the sea?", answer="Spongebob squarepants!", deck=deck)
        card.save()
        self.assertEqual(card.question, "Who lives in a pineapple under the sea?")
        self.assertEqual(card.answer, "Spongebob squarepants!")
        self.assertEqual(Card.objects.count(), 1)

    def test_card_creation_with_images(self):
        with open(self.large_image_path, 'rb') as large_img:
            large_image = SimpleUploadedFile(name='sample-large.jpg', content=large_img.read(), content_type='image/jpeg')
        
        with open(self.small_image_path, 'rb') as small_img:
            small_image = SimpleUploadedFile(name='sample-small.jpg', content=small_img.read(), content_type='image/jpeg')
        
        card = Card.objects.create(
            deck=self.deck,
            question="Test Question",
            question_image=large_image,
            answer="Test Answer",
            answer_image=small_image
        )
        card.save()

        # Verify that the large image was converted and resized
        with Image.open(card.question_image) as question_img:
            self.assertEqual(question_img.format, 'WEBP', "Large image was not converted to WEBP format.")
            self.assertTrue(question_img.width <= 800 and question_img.height <= 800, "Large image was not resized correctly.")   
        # Verify that the small images was converted but not resized
        with Image.open(card.answer_image) as answer_img:
            self.assertEqual(answer_img.format, 'WEBP', "Small image was not converted to WEBP format.")
            self.assertEqual((answer_img.width, answer_img.height), (500, 500), "Small image was resized incorrectly.")