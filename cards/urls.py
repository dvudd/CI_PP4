from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='cards-home'),
    path(
        'create_subject/',
        views.create_subject,
        name='create_subject'
    ),
    path(
        'subject/<int:subject_id>/',
        views.subject_detail,
        name='subject_detail'
    ),
    path(
        'subject/<int:subject_id>/edit/',
        views.edit_subject,
        name='edit_subject'
    ),
    path(
        'subject/<int:subject_id>/delete/',
        views.delete_subject,
        name='delete_subject'
    ),
    path(
        'subject/<int:subject_id>/create_deck/',
        views.create_deck,
        name='create_deck'
    ),
    path(
        'deck/<int:deck_id>/',
        views.deck_detail,
        name='deck_detail'
    ),
    path(
        'deck/<int:deck_id>/edit/',
        views.edit_deck,
        name='edit_deck'
    ),
    path(
        'deck/<int:deck_id>/delete/',
        views.delete_deck,
        name='delete_deck'
    ),
    path(
        'deck/<int:deck_id>/card/',
        views.manage_card,
        name='create_card'
    ),
    path(
        'deck/<int:deck_id>/card/<int:card_id>/',
        views.manage_card,
        name='edit_card'
    ),
    path(
        'card/<int:card_id>/delete/',
        views.delete_card,
        name='delete_card'
    ),
    path(
        'deck/<int:deck_id>/quiz/',
        views.quiz_view,
        name='quiz_view'
    ),
]
