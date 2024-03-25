import os
from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.urls import reverse
from PIL import Image
from .models import Subject, Deck, Card
from .forms import SubjectForm, DeckForm, CardForm


class ModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser@example.com',
            password='12345'
        )
        cls.subject = Subject.objects.create(
            name="Nostalgia",
            creator=cls.user
        )
        cls.deck = Deck.objects.create(
            name="Cartoons",
            subject=cls.subject
        )
        cls.large_image_path = os.path.join(
            settings.BASE_DIR,
            'cards/tests/test_images/sample-large.jpg'
        )
        cls.small_image_path = os.path.join(
            settings.BASE_DIR,
            'cards/tests/test_images/sample-small.jpg'
        )

    def test_subject_creation(self):
        self.assertEqual(self.subject.name, "Nostalgia")
        self.assertEqual(self.subject.creator.username, "testuser@example.com")

    def test_deck_creation(self):
        deck = Deck.objects.get(id=1)
        self.assertEqual(deck.name, "Cartoons")
        self.assertEqual(deck.subject.name, "Nostalgia")

    def test_card_creation_with_question(self):
        deck = Deck.objects.get(id=1)
        card = Card(
            question="Who lives in a pineapple under the sea?",
            answer="Spongebob squarepants!",
            deck=deck
        )
        card.save()
        self.assertEqual(
            card.question,
            "Who lives in a pineapple under the sea?"
        )
        self.assertEqual(card.answer, "Spongebob squarepants!")
        self.assertEqual(Card.objects.count(), 1)

    def test_card_creation_with_images(self):
        with open(self.large_image_path, 'rb') as large_img:
            large_image = SimpleUploadedFile(
                name='sample-large.jpg',
                content=large_img.read(),
                content_type='image/jpeg'
            )
        with open(self.small_image_path, 'rb') as small_img:
            small_image = SimpleUploadedFile(
                name='sample-small.jpg',
                content=small_img.read(),
                content_type='image/jpeg'
            )
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
            self.assertEqual(
                question_img.format,
                'WEBP', "Large image was not converted to WEBP format."
            )
            self.assertTrue(
                question_img.width <= 800 and question_img.height <= 800,
                "Large image was not resized correctly."
            )
        # Verify that the small images was converted but not resized
        with Image.open(card.answer_image) as answer_img:
            self.assertEqual(
                answer_img.format,
                'WEBP', "Small image was not converted to WEBP format."
            )
            self.assertEqual(
                (answer_img.width, answer_img.height),
                (500, 500),
                "Small image was resized incorrectly."
            )


class FormsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser@example.com',
            password='12345'
        )
        cls.large_image_path = os.path.join(
            settings.BASE_DIR,
            'cards/tests/test_images/sample-large.jpg'
        )
        cls.small_image_path = os.path.join(
            settings.BASE_DIR,
            'cards/tests/test_images/sample-small.jpg'
        )

    def test_subject_form_valid(self):
        form_data = {'name': 'Monty Python'}
        form = SubjectForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_deck_form_valid(self):
        form_data = {
            'name': 'the Holy Grail',
            'description': 'The bridge of death'
        }
        form = DeckForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_card_form_valid_with_text(self):
        form_data = {
            'question': 'What is your name?',
            'answer': 'It is Arthur, King of the Britons.'
        }
        form = CardForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_card_form_valid_with_image(self):
        with open(self.large_image_path, 'rb') as large_img:
            large_image = SimpleUploadedFile(
                name='sample-large.jpg',
                content=large_img.read(),
                content_type='image/jpeg'
            )
        with open(self.small_image_path, 'rb') as small_img:
            small_image = SimpleUploadedFile(
                name='sample-small.jpg',
                content=small_img.read(),
                content_type='image/jpeg'
            )
        form_data = {
            'question': 'What is your quest?',
            'question_image': large_image,
            'answer': 'To seek the Holy Grail.',
            'answer_image': small_image
        }
        form = CardForm(
            data=form_data,
            files={
                'question_image': large_image,
                'answer_image': small_image
            })
        self.assertTrue(form.is_valid())

    def test_card_form_invalid(self):
        form_data = {}
        form = CardForm(data=form_data)
        self.assertFalse(form.is_valid())


class HomeViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser@example.com',
            password='12345'
        )
        cls.subject1 = Subject.objects.create(
            name="Test Subject 1",
            creator=cls.user
        )
        cls.subject2 = Subject.objects.create(
            name="Test Subject 2",
            creator=cls.user
        )
        cls.subject3 = Subject.objects.create(
            name="Test Subject 3",
            creator=cls.user
        )

    def test_home_view_authenticated(self):
        self.client.login(
            username='testuser@example.com',
            password='12345'
        )
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


class SubjectViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser@example.com',
            password='12345'
        )
        self.client.login(
            username='testuser@example.com',
            password='12345'
        )
        self.subject = Subject.objects.create(
            name="Test Subject",
            creator=self.user
        )

    def test_create_subject(self):
        response = self.client.get(reverse('create_subject'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/subject_create.html')
        response = self.client.post(reverse(
            'create_subject'),
            {'name': 'New Subject'}
        )
        self.assertEqual(Subject.objects.count(), 2)
        self.assertRedirects(response, reverse(
            'subject_detail',
            args=[Subject.objects.latest('id').id])
        )

    def test_subject_detail(self):
        response = self.client.get(reverse(
            'subject_detail',
            args=[self.subject.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/subject_detail.html')

    def test_edit_subject(self):
        response = self.client.get(reverse(
            'edit_subject',
            args=[self.subject.id])
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse(
            'edit_subject',
            args=[self.subject.id]),
            {'name': 'Updated Subject'}
        )
        self.subject.refresh_from_db()
        self.assertEqual(self.subject.name, 'Updated Subject')
        self.assertRedirects(response, reverse(
            'subject_detail',
            args=[self.subject.id])
        )

    def test_delete_subject(self):
        response = self.client.post(reverse(
            'delete_subject',
            args=[self.subject.id])
        )
        self.assertEqual(Subject.objects.count(), 0)
        self.assertRedirects(response, reverse('cards-home'))


class DeckViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser@example.com',
            password='12345'
        )
        self.subject = Subject.objects.create(
            name="Test Subject",
            creator=self.user
        )
        self.deck = Deck.objects.create(
            name="Test Deck",
            subject=self.subject
        )
        self.client.login(
            username='testuser@example.com',
            password='12345'
        )

    def test_create_deck(self):
        response = self.client.get(reverse(
            'create_deck',
            args=[self.subject.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/deck_create.html')

    def test_deck_detail(self):
        response = self.client.get(reverse(
            'deck_detail',
            args=[self.deck.id])
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse(
            'edit_deck',
            args=[self.deck.id]),
            {'name': 'Updated Deck'}
        )
        self.deck.refresh_from_db()
        self.assertEqual(self.deck.name, 'Updated Deck')
        self.assertRedirects(response, reverse(
            'deck_detail',
            args=[self.deck.id])
        )

    def test_edit_deck(self):
        response = self.client.get(reverse('edit_deck', args=[self.deck.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/deck_edit.html')

    def test_delete_deck(self):
        response = self.client.post(reverse(
            'delete_deck',
            args=[self.deck.id])
        )
        self.assertRedirects(response, reverse(
            'subject_detail',
            args=[self.subject.id])
        )
        with self.assertRaises(Deck.DoesNotExist):
            Deck.objects.get(id=self.deck.id)


class CardViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser@example.com',
            password='12345'
        )
        self.subject = Subject.objects.create(
            name="Test Subject",
            creator=self.user
        )
        self.deck = Deck.objects.create(
            name="Test Deck",
            subject=self.subject
        )
        self.card = Card.objects.create(
            question="Test Question",
            answer="Test Answer",
            deck=self.deck
        )
        self.client.login(
            username='testuser@example.com',
            password='12345'
        )

    def test_create_card(self):
        response = self.client.get(reverse(
            'create_card',
            args=[self.deck.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/card_create.html')

    def test_card_detail(self):
        response = self.client.get(reverse('card_detail', args=[self.card.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/card_detail.html')

    def test_edit_card(self):
        response = self.client.get(reverse('edit_card', args=[self.card.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/card_edit.html')
        post_response = self.client.post(reverse(
            'edit_card',
            args=[self.card.id]),
            {'question': 'Updated Question', 'answer': 'Updated Answer'}
        )
        self.card.refresh_from_db()
        self.assertEqual(self.card.question, 'Updated Question')
        self.assertEqual(self.card.answer, 'Updated Answer')
        self.assertRedirects(post_response, reverse(
            'card_detail',
            args=[self.card.id])
        )

    def test_delete_card(self):
        response = self.client.post(reverse(
            'delete_card',
            args=[self.card.id])
        )
        self.assertRedirects(response, reverse(
            'deck_detail',
            args=[self.deck.id])
        )
        with self.assertRaises(Card.DoesNotExist):
            Card.objects.get(id=self.card.id)


class QuizViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser@example.com',
            password='12345'
        )
        self.subject = Subject.objects.create(
            name="Test Subject",
            creator=self.user
        )
        self.deck = Deck.objects.create(
            name="Test Deck",
            subject=self.subject
        )
        self.card1 = Card.objects.create(
            question="Test Question 1",
            answer="Test Answer 1",
            deck=self.deck
        )
        self.card2 = Card.objects.create(
            question="Test Question 2",
            answer="Test Answer 2",
            deck=self.deck
        )
        self.client.login(
            username='testuser@example.com',
            password='12345'
        )

    def test_quiz_access(self):
        response = self.client.get(reverse(
            'quiz_view',
            args=[self.deck.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/quiz.html')

    def test_quiz_context(self):
        response = self.client.get(reverse(
            'quiz_view',
            args=[self.deck.id])
        )
        self.assertIn('deck', response.context)
        self.assertIn('cards', response.context)
        self.assertEqual(len(response.context['cards']), 2)
        self.assertEqual(response.context['deck'], self.deck)
