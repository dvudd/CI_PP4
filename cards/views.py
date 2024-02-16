from django.shortcuts import render, redirect, get_object_or_404
from .forms import SubjectForm, DeckForm, CardForm
from .models import Subject, Deck, Card

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        # Render a template with user-specific content for logged-in users
        user_subjects = Subject.objects.filter(creator=request.user)
        return render(request, 'cards/home.html', {'user_subjects': user_subjects})
    else:
        # Render a generic template (index.html) for non-logged-in users
        return render(request, 'cards/index.html')


def create_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.creator = request.user
            subject.save()
            return redirect('subject_detail', subject_id=subject.id)
    else:
        form = SubjectForm()
    return render(request, 'cards/create_subject.html', {'form': form})

def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    return render(request, 'cards/subject_detail.html', {'subject': subject})

def create_deck(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        form = DeckForm(request.POST)
        if form.is_valid():
            deck = form.save(commit=False)
            deck.subject = subject
            deck.save()
            return redirect('deck_detail', deck_id=deck.id)
    else:
        form = DeckForm()
    return render(request, 'cards/create_deck.html', {'form': form, 'subject': subject})

def deck_detail(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    cards = deck.card_set.all()  # Retrieve all cards related to this deck
    return render(request, 'cards/deck_detail.html', {'deck': deck, 'cards': cards})

def create_card(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.deck = deck
            card.save()
            return redirect('card_detail', card_id=card.id)
    else:
        form = CardForm()
    return render(request, 'cards/create_card.html', {'form': form, 'deck': deck})

def card_detail(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    return render(request, 'cards/card_detail.html', {'card': card})