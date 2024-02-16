from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='cards-home'),
    path('create_subject/', views.create_subject, name='create_subject'),
    path('subject/<int:subject_id>/', views.subject_detail, name='subject_detail'),
]