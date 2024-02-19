from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='cards-home'),
    path('create_subject/', views.create_subject, name='create_subject'),
    path('subject/<int:subject_id>/', views.subject_detail, name='subject_detail'),
    path('subject/<int:subject_id>/edit/', views.edit_subject, name='edit_subject'),
    path('subject/<int:subject_id>/create_deck/', views.create_deck, name='create_deck'),
    path('deck/<int:deck_id>/', views.deck_detail, name='deck_detail'),
    path('subject/<int:deck_id>/create_card/', views.create_card, name='create_card'),
    path('card/<int:card_id>/', views.card_detail, name='card_detail'),
]