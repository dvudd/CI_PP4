from django.test import TestCase
from django.contrib.auth.models import User
from .models import Subject, Deck, Card

class ModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user
        test_user = User.objects.create_user(username='testuser', password='12345')
        test_user.save()
        # Create a subject
        test_subject = Subject.objects.create(name="Nostalgia", creator=test_user)
        # Create a deck
        test_deck = Deck.objects.create(name="Cartoons", description="Cartoons from your childhood", subject=test_subject)

    def test_subject_creation(self):
        subject = Subject.objects.get(id=1)
        self.assertEqual(subject.name, "Nostalgia")
        self.assertEqual(subject.creator.username, "testuser")

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