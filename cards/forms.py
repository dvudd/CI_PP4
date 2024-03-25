from django import forms
from .models import Subject, Deck, Card


class SubjectForm(forms.ModelForm):
    """
    A form for creating and updating Subject instances.
    """
    class Meta:
        model = Subject
        fields = ['name']


class DeckForm(forms.ModelForm):
    """
    A form for creating and updating Deck instances.
    """
    class Meta:
        model = Deck
        fields = ['name', 'description']


class CardForm(forms.ModelForm):
    """
    A form for creating and updating Card instances.
    """
    class Meta:
        model = Card
        fields = ['question', 'question_image', 'answer', 'answer_image']
