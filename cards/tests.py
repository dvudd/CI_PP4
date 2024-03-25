import os
from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from PIL import Image
from django.urls import reverse
from .models import Subject, Deck, Card
from .forms import SubjectForm, DeckForm, CardForm

class ModelsTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create_user(username='testuser@example.com', password='12345')
        self.subject = Subject.objects.create(name="Nostalgia", creator=self.user)
        self.deck = Deck.objects.create(name="Cartoons", subject=self.subject)
        self.large_image_path = os.path.join(settings.BASE_DIR, 'cards/tests/test_images/sample-large.jpg')
        self.small_image_path = os.path.join(settings.BASE_DIR, 'cards/tests/test_images/sample-small.jpg')

    def test_subject_creation(self):
        self.assertEqual(self.subject.name, "Nostalgia")
        self.assertEqual(self.subject.creator.username, "testuser@example.com")

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

class FormsTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create_user(username='testuser@example.com', password='12345')
        self.large_image_path = os.path.join(settings.BASE_DIR, 'cards/tests/test_images/sample-large.jpg')
        self.small_image_path = os.path.join(settings.BASE_DIR, 'cards/tests/test_images/sample-small.jpg')

    def test_subject_form_valid(self):
        form_data = {'name': 'Monty Python'}
        form = SubjectForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_deck_form_valid(self):
        form_data = {'name': 'the Holy Grail', 'description': 'The bridge of death'}
        form = DeckForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_card_form_valid_with_text(self):
        form_data = {'question': 'What is your name?', 'answer': 'It is Arthur, King of the Britons.'}
        form = CardForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_card_form_valid_with_image(self):
        with open(self.large_image_path, 'rb') as large_img:
            large_image = SimpleUploadedFile(name='sample-large.jpg', content=large_img.read(), content_type='image/jpeg')
        
        with open(self.small_image_path, 'rb') as small_img:
            small_image = SimpleUploadedFile(name='sample-small.jpg', content=small_img.read(), content_type='image/jpeg')
        
        form_data = {'question': 'What is your quest?', 'question_image': large_image, 'answer': 'To seek the Holy Grail.', 'answer_image': small_image}
        form = CardForm(data=form_data, files={'question_image': large_image, 'answer_image': small_image})
        self.assertTrue(form.is_valid())

    def test_card_form_invalid(self):
        form_data = {}
        form = CardForm(data=form_data)
        self.assertFalse(form.is_valid())

class HomeViewTests(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = get_user_model().objects.create_user(username='testuser@example.com', password='12345')
        self.subject1 = Subject.objects.create(name="Test Subject 1", creator=self.user)
        self.subject2 = Subject.objects.create(name="Test Subject 2", creator=self.user)
        self.subject3 = Subject.objects.create(name="Test Subject 3", creator=self.user)

    def test_home_view_authenticated(self):
        self.client.login(username='testuser@example.com', password='12345')
        response = self.client.get(reverse('cards-home'))
        self.assertTemplateUsed(response, 'cards/home.html')
        self.assertIn('user_subjects', response.context)
        user_subjects = response.context['user_subjects']
        self.assertTrue(self.subject1 in user_subjects)
        self.assertTrue(self.subject2 in user_subjects)
        self.assertTrue(self.subject3 in user_subjects)

    def test_home_view_unauthenticated(self):
        response = self.client.get(reverse('cards-home'))
        self.assertTemplateUsed(response, 'cards/index.html')
        self.assertNotIn('user_subjects', response.context)