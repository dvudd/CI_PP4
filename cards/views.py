from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import SubjectForm, DeckForm, CardForm
from .models import Subject, Deck, Card
from django.core.serializers import serialize
import json

# Home view
def home(request):
    """
    Render the home page of the application.

    For authenticated users, this view displays a list of subjects created by them.
    For non-authenticated users, a generic welcome page is displayed.
    """
    if request.user.is_authenticated:
        # Render a template with user-specific content for logged-in users
        user_subjects = Subject.objects.filter(creator=request.user)
        return render(request, 'cards/home.html', {'user_subjects': user_subjects})
    else:
        # Render a generic template (index.html) for non-logged-in users
        return render(request, 'cards/index.html')

# SUBJECTS

# Create Subject
@login_required
def create_subject(request):
    """
    Create a new subject.

    Allows a logged-in user to create a new subject. The user is redirected
    to the subject detail page upon successful creation
    """
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.creator = request.user
            subject.save()
            return redirect('subject_detail', subject_id=subject.id)
    else:
        form = SubjectForm()
    return render(request, 'cards/subject_create.html', {'form': form})

# Subject Details
@login_required
def subject_detail(request, subject_id):
    """
    Display the details of a specific subject.

    Retrieves and displays details of a subject only if the
    logged in user is the creator of the subject, if not the
    user is denied access.
    """
    subject = get_object_or_404(Subject, id=subject_id, creator=request.user)
    return render(request, 'cards/subject_detail.html', {'subject': subject})

# Edit Subject
@login_required
def edit_subject(request, subject_id):
    """
    Edit an existing subject.

    Allows the creator of the subject to edit its details.
    After a successful edit the user is redirected to the
    detail page.
    """
    subject = get_object_or_404(Subject, id=subject_id, creator=request.user)

    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('subject_detail', subject_id=subject.id)
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'cards/subject_edit.html', {'form': form, 'subject': subject})

# Delete Subject
@login_required
def delete_subject(request, subject_id):
    """
    Delete a existing subject.

    Allows the creator of the subject to delete the subject
    with all the decks/cards belonging to it. After a
    successful deletion, the user is redirected to the
    home page.
    """
    subject = get_object_or_404(Subject, id=subject_id, creator=request.user)

    subject.delete()
    messages.success(request, "Subject deleted successfully")
    return redirect('cards-home')

# DECKS

# Create Deck
@login_required
def create_deck(request, subject_id):
    """
    Create a new deck.

    Allows a logged-in user to create a new deck. The user is redirected
    to the deck detail page upon successful creation
    """
    subject = get_object_or_404(Subject, id=subject_id, creator=request.user)

    if request.method == 'POST':
        form = DeckForm(request.POST)
        if form.is_valid():
            deck = form.save(commit=False)
            deck.subject = subject
            deck.save()
            return redirect('deck_detail', deck_id=deck.id)
    else:
        form = DeckForm()
    return render(request, 'cards/deck_create.html', {'form': form, 'subject': subject})

# Deck Details
def deck_detail(request, deck_id):
    """
    Display the details of a specific deck.

    Retrieves and displays details of a deck only if the
    logged in user is the creator of the subject, if not the
    user is denied access.
    """
    deck = get_object_or_404(Deck, id=deck_id, subject__creator=request.user)
    cards = deck.card_set.all()
    num_cards = deck.card_set.count()
    return render(request, 'cards/deck_detail.html', {'deck': deck, 'cards': cards, 'num_cards': num_cards})

# Edit Deck
@login_required
def edit_deck(request, deck_id):
    """
    Edit an existing deck.

    Allows the creator of the subject to edit the decks details.
    After a successful edit the user is redirected to the
    detail page.
    """
    deck = get_object_or_404(Deck, id=deck_id, subject__creator=request.user)

    cards = deck.card_set.all()
    if request.method == 'POST':
        form = DeckForm(request.POST, instance=deck)
        if form.is_valid():
            form.save()
            return redirect('deck_detail', deck_id=deck.id)
    else:
        form = DeckForm(instance=deck)
    return render(request, 'cards/deck_edit.html', {'form': form, 'deck': deck, 'cards': cards,})

# Delete Deck
@login_required
def delete_deck(request, deck_id):
    """
    Delete a existing deck.

    Allows the creator of the subject to delete the deck
    with all the cards belonging to it. After a
    successful deletion, the user is redirected to the
    subject detail page.
    """
    deck = get_object_or_404(Deck, id=deck_id, subject__creator=request.user)

    deck.delete()
    messages.success(request, "Deck deleted successfully")
    return redirect('subject_detail', subject_id=deck.subject.id)

# CARDS

# Create Card
@login_required
def create_card(request, deck_id):
    """
    Create a new card.

    Allows a logged-in user to create a new card. The user is redirected
    to the deck detail page upon successful creation
    """
    deck = get_object_or_404(Deck, id=deck_id, subject__creator=request.user)

    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES)
        if form.is_valid():
            card = form.save(commit=False)
            card.deck = deck
            card.save()
            return redirect('card_detail', card_id=card.id)
    else:
        form = CardForm()
    return render(request, 'cards/card_create.html', {'form': form, 'deck': deck})

# Card Details
def card_detail(request, card_id):
    """
    Display the details of a specific card.

    Retrieves and displays details of a card only if the
    logged in user is the creator of the subject, if not the
    user is denied access.
    """
    card = get_object_or_404(Card, id=card_id, deck__subject__creator=request.user)
    return render(request, 'cards/card_detail.html', {'card': card})

# Edit Card
@login_required
def edit_card(request, card_id):
    """
    Edit an existing card.

    Allows the creator of the subject to edit the cards details.
    After a successful edit the user is redirected to the
    detail page.
    """
    card = get_object_or_404(Card, id=card_id, deck__subject__creator=request.user)

    if request.method == 'POST':
        form = CardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            return redirect('card_detail', card_id=card.id)
    else:
        form = CardForm(instance=card)
    return render(request, 'cards/card_edit.html', {'form': form, 'card': card})

# Delete Card
@login_required
def delete_card(request, card_id):
    """
    Delete a existing card.

    Allows the creator of the subject to delete the card.
    After a successful deletion, the user is redirected to the
    subject detail page.
    """
    card = get_object_or_404(Card, id=card_id, deck__subject__creator=request.user)

    card.delete()
    messages.success(request, "Card deleted successfully")
    return redirect('deck_detail', deck_id=card.deck.id)

# Quiz view
@login_required
def quiz_view(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id, subject__creator=request.user)

    cards = deck.card_set.all()
    data = []
    for card in cards:
        card_data = {
            'question': card.question,
            'answer': card.answer,
            'question_image': request.build_absolute_uri(card.question_image.url) if card.question_image else '',
            'answer_image': request.build_absolute_uri(card.answer_image.url) if card.answer_image else '',
        }
        data.append(card_data)
    return render(request, 'cards/quiz.html', {'deck': deck, 'cards': data})
