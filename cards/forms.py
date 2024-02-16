from django import forms
from .models import Subject, Deck, Card

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name']

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['question', 'answer']