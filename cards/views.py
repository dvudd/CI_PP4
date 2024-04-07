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

    For authenticated users, this view displays a list of subjects
    created by them.
    For non-authenticated users, a generic welcome page is displayed.
    """
    if request.user.is_authenticated:
        # Render a template with user-specific content for logged-in users
        user_subjects = Subject.objects.filter(creator=request.user)
        return render(
            request,
            'cards/home.html',
            {'user_subjects': user_subjects}
        )
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
    return render(
        request,
        'cards/subject_edit.html',
        {'form': form, 'subject': subject}
    )


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
    return render(
        request,
        'cards/deck_create.html',
        {'form': form, 'subject': subject}
    )


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
    return render(
        request,
        'cards/deck_detail.html',
        {'deck': deck, 'cards': cards, 'num_cards': num_cards}
    )


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

    if request.method == 'POST':
        form = DeckForm(request.POST, instance=deck)
        if form.is_valid():
            form.save()
            return redirect('deck_detail', deck_id=deck.id)
    else:
        form = DeckForm(instance=deck)
    num_cards = deck.card_set.count()
    return render(
        request,
        'cards/deck_edit.html',
        {'form': form, 'deck': deck, 'num_cards': num_cards}
    )


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
# Create and update Card
@login_required
def manage_card(request, deck_id, card_id=None):
    """
    Handles creation and updating of cards.

    If a card ID is provided, the view functions as an edit form for the
    specified card.
    If no card ID is provided, the view presents a form
    for creating a new card.
    """
    deck = get_object_or_404(Deck, id=deck_id, subject__creator=request.user)
    if card_id:
        card = get_object_or_404(Card, id=card_id, deck=deck)
        action = "Edit"
    else:
        card = None
        action = "Create"

    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            card = form.save(commit=False)
            card.deck = deck
            card.save()
            form = CardForm()
    else:
        form = CardForm(instance=card)
    cards = Card.objects.filter(deck=deck).order_by('-created_at')
    return render(request, 'cards/card_form.html', {
        'form': form,
        'deck': deck,
        'cards': cards,
        'action': action
    })


# Delete Card
@login_required
def delete_card(request, card_id):
    """
    Delete an existing card.

    Allows the creator of the subject to delete the card.
    After a successful deletion, the user is redirected back to the
    create card page to continue managing other cards within the deck.
    """
    card = get_object_or_404(
        Card,
        id=card_id,
        deck__subject__creator=request.user
    )
    deck_id = card.deck.id
    card.delete()
    messages.success(request, "Card deleted successfully")
    return redirect('create_card', deck_id=deck_id)


# Quiz view
@login_required
def quiz_view(request, deck_id):
    """
    Renders the quiz page with a set of cards from a specified deck.
    Ensures that all necessary content is available for front-end parsing.
    """
    deck = get_object_or_404(Deck, pk=deck_id, subject__creator=request.user)
    cards = deck.card_set.all()
    data = []
    for card in cards:
        if card.question_image:
            question_img = request.build_absolute_uri(card.question_image.url)
        else:
            question_img = ''
        if card.answer_image:
            answer_img = request.build_absolute_uri(card.answer_image.url)
        else:
            answer_img = ''
        card_data = {
            'question': card.question,
            'answer': card.answer,
            'question_image': question_img,
            'answer_image': answer_img
        }
        data.append(card_data)
    return render(request, 'cards/quiz.html', {'deck': deck, 'cards': data})
