"""
URL configuration for flashcards project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from users import views as user_views
from cards import views as cards_views

urlpatterns = [
    path('', include('cards.urls')),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.user_login, name='login'),
    path(
        'logout/',
        auth_views.LogoutView.as_view(template_name='logout.html'),
        name='logout'
    ),
    path('profile/', user_views.profile, name='profile'),
]

# Custom error handlers
handler404 = 'cards.views.handler404'

# Enable admin page when DEBUG is set to True
if settings.DEBUG == 'True':
    urlpatterns += path('admin/', admin.site.urls),
