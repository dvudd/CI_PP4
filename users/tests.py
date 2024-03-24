import os
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from PIL import Image
from .models import Profile

class UserTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test@example.com', password='testpass123')
        self.large_image_path = os.path.join(settings.BASE_DIR, 'cards/tests/test_images/sample-large.jpg')

    def test_profile_creation(self):
        user_profile = self.user.profile
        self.assertIsNotNone(user_profile)


    def test_register_user(self):
        response = self.client.post(reverse('register'), data={
            'email': 'newuser@example.com',
            'first_name': 'First',
            'last_name': 'Last',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())
        self.assertTrue(User.objects.filter(username='newuser@example.com').exists())

    def test_login_user(self):
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get(reverse('cards-home'))
        self.assertEqual(str(response.context['user']), 'test@example.com')

    def test_update_profile(self):
        self.client.login(username='test@example.com', password='testpass123')
        with open(self.large_image_path, 'rb') as large_img:
            large_image = SimpleUploadedFile(name='sample-large.jpg', content=large_img.read(), content_type='image/jpeg')

        response = self.client.post(reverse('profile'), data={
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
            'image': large_image,
        }, follow=True)

        # Reload the user and profile from the database to get the updated values
        self.user.refresh_from_db()
        profile = self.user.profile
        profile.refresh_from_db()

        # Verify the email was updated
        self.assertEqual(self.user.email, 'updated@example.com')

        # Verify that the profile image was converted and resized
        with Image.open(profile.image) as profile_img:
            self.assertEqual(profile_img.format, 'WEBP', "Large image was not converted to WEBP format.")
            self.assertTrue(profile_img.width <= 300 and profile_img.height <= 300, "Large image was not resized correctly.")

