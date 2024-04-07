import os
from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError
from PIL import Image
from .models import Subject, Deck, Card
from .forms import SubjectForm, DeckForm, CardForm


class ModelsTest(TestCase):
    """
    Tests for validating the creation and functionality of Subject, Deck, and
    Card models.
    This class includes tests that ensure the models are correctly created and
    associated with each other, and that image processing (resizing and format
    conversion) is handled as expected.
    """
    def setUp(self):
        """
        Set up data for the test case.
        """
        self.user = User.objects.create_user(
            username='testuser@example.com',
            password='12345'
        )
        self.subject = Subject.objects.create(
            name="Nostalgia",
            creator=self.user
        )
        self.deck = Deck.objects.create(
            name="Cartoons",
            subject=self.subject
        )
        self.large_image_path = os.path.join(
            settings.BASE_DIR,
            'cards/tests/test_images/sample-large.jpg'
        )
        self.small_image_path = os.path.join(
            settings.BASE_DIR,
            'cards/tests/test_images/sample-small.jpg'
        )

    def test_subject_creation(self):
        """
        Tests the creation of a Subject.
        """
        self.assertEqual(self.subject.name, "Nostalgia")
        self.assertEqual(self.subject.creator.username, "testuser@example.com")

    def test_subject_str(self):
        """
        Test the string representation of the Subject model.
        """
        self.assertEqual(str(self.subject), "Nostalgia")

    def test_deck_creation(self):
        """
        Tests the creation of a Deck.
        """
        deck = Deck.objects.get(id=1)
        self.assertEqual(deck.name, "Cartoons")
        self.assertEqual(deck.subject.name, "Nostalgia")

    def test_deck_str(self):
        """
        Test the string representation of the Deck model.
        """
        self.assertEqual(str(self.deck), "Cartoons")

    def test_card_creation_with_question(self):
        """
        Tests the creation of a Card with text as question and answer.
        """
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
        """
        Tests the creation of a Card using an image as both the question
        and the answer.
        The question image is 1000x1000px and will be resized to 800x800px.
        The answer image is 500x500px and will not be resized.
        Both images will be converted to .webp
        """
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

    def test_card_clean_without_question(self):
        """
        Test that a ValidationError is raised if a card is created without
        a question.
        """
        card = Card(deck=self.deck, answer="Test Answer")
        with self.assertRaises(ValidationError):
            card.clean()

    def test_card_clean_without_answer(self):
        """
        Test that a ValidationError is raised if a card is created without
        an answer.
        """
        card = Card(deck=self.deck, question="Test Question")
        with self.assertRaises(ValidationError):
            card.clean()


class FormsTest(TestCase):
    """
    Tests for the validity of form data in the cards app.
    This class focuses on verifying the forms used for creating
    subjects, decks, and cards within the application.
    """
    def setUp(self):
        """
        Set up data for the test case.
        """
        self.user = User.objects.create_user(
            username='testuser@example.com',
            password='12345'
        )
        self.large_image_path = os.path.join(
            settings.BASE_DIR,
            'cards/tests/test_images/sample-large.jpg'
        )
        self.small_image_path = os.path.join(
            settings.BASE_DIR,
            'cards/tests/test_images/sample-small.jpg'
        )

    def test_subject_form_valid(self):
        """
        Test the SubjectForm with valid data.
        """
        form_data = {'name': 'Monty Python'}
        form = SubjectForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_deck_form_valid(self):
        """
        Test the DeckForm with valid data.
        """
        form_data = {
            'name': 'the Holy Grail',
            'description': 'The bridge of death'
        }
        form = DeckForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_card_form_valid_with_text(self):
        """
        Test the CardForm with valid data.
        """
        form_data = {
            'question': 'What is your name?',
            'answer': 'It is Arthur, King of the Britons.'
        }
        form = CardForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_card_form_valid_with_image(self):
        """
        Test the CardForm with valid image data.
        """
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
        """
        Test the CardForm with invalid data.
        """
        form_data = {}
        form = CardForm(data=form_data)
        self.assertFalse(form.is_valid())


class HomeViewTests(TestCase):
    """
    Tests for the home view.
    This class tests the behavior for authenticated and unauthenticated
    users, ensuring that the correct template is used and that the appropriate
    context data is provided.
    """
    def setUp(self):
        """
        Set up data for the test case.
        """
        self.user = get_user_model().objects.create_user(
            username='testuser@example.com',
            password='12345'
        )
        self.subject1 = Subject.objects.create(
            name="Test Subject 1",
            creator=self.user
        )
        self.subject2 = Subject.objects.create(
            name="Test Subject 2",
            creator=self.user
        )
        self.subject3 = Subject.objects.create(
            name="Test Subject 3",
            creator=self.user
        )

    def test_home_view_authenticated(self):
        """
        Test the home view with an authenticated user.
        Verifies that the correct template is used and that the user's
        subjects are correctly passed to the template.
        """
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
        """
        Test the home view with an unauthenticated user.
        Checks that the correct template is used and that no user-specific
        content is provided.
        """
        response = self.client.get(reverse('cards-home'))
        self.assertTemplateUsed(response, 'cards/index.html')
        self.assertNotIn('user_subjects', response.context)

    def test_404_view(self):
        """
        Tests the 404 page.
        """
        response = self.client.get('/non-existent-page/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'cards/404.html')


class SubjectViewTests(TestCase):
    """
    Tests for the subject view.
    This class tests creating, viewing, editing, and deleting subjects.
    """
    def setUp(self):
        """
        Set up a user and creates a subject associated with that user.
        """
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
        """
        Test the creation of a subject.
        """
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
        """
        Test the display of a subject's detail view.
        """
        response = self.client.get(reverse(
            'subject_detail',
            args=[self.subject.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/subject_detail.html')

    def test_edit_subject(self):
        """
        Test the editing of a subject.
        """
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
        """
        Test the deletion of a subject.
        """
        response = self.client.post(reverse(
            'delete_subject',
            args=[self.subject.id])
        )
        self.assertEqual(Subject.objects.count(), 0)
        self.assertRedirects(response, reverse('cards-home'))


class DeckViewTests(TestCase):
    """
    Tests for the deck view.
    This class tests creating, viewing, editing, and deleting decks.
    """
    def setUp(self):
        """
        Set up a user and creates a subject and a deck associated with
        that user.
        """
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
        """
        Test the creation of a deck.
        """
        response = self.client.get(reverse(
            'create_deck',
            args=[self.subject.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/deck_create.html')

    def test_create_deck_post(self):
        """
        Test the creation of a deck via POST request.
        """
        decks_before = Deck.objects.count()
        post_data = {
            'name': 'New Deck',
            'description': 'A new test deck',
        }
        response = self.client.post(reverse(
            'create_deck',
            args=[self.subject.id]),
            post_data
        )
        self.assertEqual(Deck.objects.count(), decks_before + 1)
        new_deck = Deck.objects.latest('id')
        self.assertEqual(new_deck.subject, self.subject)
        self.assertRedirects(response, reverse(
            'deck_detail',
            args=[new_deck.id]
        ))

    def test_deck_detail(self):
        """
        Test the display of a decks's detail view.
        """
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
        """
        Test the editing of a deck.
        """
        response = self.client.get(reverse('edit_deck', args=[self.deck.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/deck_edit.html')

    def test_delete_deck(self):
        """
        Test the deletion of a deck.
        """
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
    """
    Tests for the card view.
    This class tests creating, viewing, editing, and deleting cards.
    """
    def setUp(self):
        """
        Set up a user and creates a subject, deck and a card associated
        with that user.
        """
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
        """
        Test the creation of a card.
        """
        response = self.client.get(reverse(
            'create_card',
            args=[self.deck.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/card_form.html')

    def test_card_submission(self):
        """
        Test the submission of a new card.
        """
        response = self.client.post(reverse(
            'create_card',
            args=[self.deck.id]),
            {
                'question': 'New Question', 'answer': 'New Answer'
            }
        )
        self.assertEqual(Card.objects.count(), 2)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/card_form.html')

    def test_edit_card(self):
        """
        Test the editing of a card.
        """
        self.client.login(
            username='testuser@example.com',
            password='12345'
        )
        card_initial_question = self.card.question
        card_initial_answer = self.card.answer
        updated_question = 'Updated Question'
        updated_answer = 'Updated Answer'

        response = self.client.post(reverse(
            'edit_card',
            args=[
                self.deck.id,
                self.card.id]),
            {
                'question': updated_question,
                'answer': updated_answer
            },
            follow=True)
        self.assertEqual(response.status_code, 200)
        self.card.refresh_from_db()
        self.assertNotEqual(self.card.question, card_initial_question)
        self.assertNotEqual(self.card.answer, card_initial_answer)
        self.assertEqual(self.card.question, updated_question)
        self.assertEqual(self.card.answer, updated_answer)
        self.assertTemplateUsed(response, 'cards/card_form.html')

    def test_delete_card(self):
        """
        Test the deletion of a card.
        """
        response = self.client.post(reverse(
            'delete_card',
            args=[self.card.id])
        )
        self.assertRedirects(response, reverse(
            'create_card',
            args=[self.deck.id])
        )
        with self.assertRaises(Card.DoesNotExist):
            Card.objects.get(id=self.card.id)


class QuizViewTest(TestCase):
    """
    Tests for the quiz view.
    This class tests viewing the quiz
    """
    def setUp(self):
        """
        Set up a user and creates a subject, deck and a couple of cards
        associated with that user.
        """
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
        """
        Tests the access of the quiz
        """
        response = self.client.get(reverse(
            'quiz_view',
            args=[self.deck.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/quiz.html')

    def test_quiz_context(self):
        """
        Tests that the correct cards are presented.
        """
        response = self.client.get(reverse(
            'quiz_view',
            args=[self.deck.id])
        )
        self.assertIn('deck', response.context)
        self.assertIn('cards', response.context)
        self.assertEqual(len(response.context['cards']), 2)
        self.assertEqual(response.context['deck'], self.deck)
