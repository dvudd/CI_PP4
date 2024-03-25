import os
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from PIL import Image
from .models import Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


class ModelsTest(TestCase):
    """
    Tests the user model and profile model functionality.
    """
    def setUp(self):
        """
        Set up a user and specifies the path to a large image.
        """
        self.user = User.objects.create_user(
            username='test@example.com',
            password='testpass123'
        )
        self.large_image_path = os.path.join(
            settings.BASE_DIR,
            'cards/tests/test_images/sample-large.jpg'
        )

    def test_profile_creation(self):
        """
        Tests that a profile is automatically created for a new user
        """
        user_profile = self.user.profile
        self.assertIsNotNone(user_profile)

    def test_register_user(self):
        """
        Tests that a new user can be registered.
        """
        response = self.client.post(reverse('register'), data={
            'email': 'newuser@example.com',
            'first_name': 'First',
            'last_name': 'Last',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(
            email='newuser@example.com').exists()
        )
        self.assertTrue(User.objects.filter(
            username='newuser@example.com').exists()
        )

    def test_login_user(self):
        """
        Tests that a user can login
        """
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get(reverse('cards-home'))
        self.assertEqual(str(response.context['user']), 'test@example.com')

    def test_update_profile(self):
        """
        Tests the funcionality of updating user profile.
        Including changing user details and uploading a profile image.
        The image used is 1000x1000px and should be resized to 300x300px
        The image should also be converted to .webp
        """
        self.client.login(username='test@example.com', password='testpass123')
        with open(self.large_image_path, 'rb') as large_img:
            large_image = SimpleUploadedFile(
                name='sample-large.jpg',
                content=large_img.read(),
                content_type='image/jpeg'
            )

        response = self.client.post(reverse('profile'), data={
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
            'image': large_image,
        }, follow=True)

        self.user.refresh_from_db()
        profile = self.user.profile
        profile.refresh_from_db()

        self.assertEqual(self.user.email, 'updated@example.com')

        # Verify that the profile image was converted and resized
        with Image.open(profile.image) as profile_img:
            self.assertEqual(
                profile_img.format,
                'WEBP',
                "Large image was not converted to WEBP format."
            )
            self.assertTrue(
                profile_img.width <= 300 and profile_img.height <= 300,
                "Large image was not resized correctly."
            )


class FormsTest(TestCase):
    """
    Tests for the validity of form data in the users app.
    This class focuses on verifying the forms used for user creation and
    profile updating.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the test case.
        """
        cls.user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='testpass123'
        )
        cls.profile = Profile.objects.get(user=cls.user)
        cls.large_image_path = os.path.join(
            settings.BASE_DIR,
            'cards/tests/test_images/sample-large.jpg'
        )

    def test_user_register_form_valid(self):
        """
        Test the user registration with valid data
        """
        form_data = {
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_register_form_invalid(self):
        """
        Test the user registration with invalid data
        """
        form_data = {
            'email': 'notanemail',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_user_register_form_duplicate_email(self):
        """
        Test the user registration with an existing email
        """
        form_data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_user_update_form_valid(self):
        """
        Test the user update form with valid data
        """
        form_data = {
            'email': 'updated@example.com',
            'first_name': 'UpdatedFirstName',
            'last_name': 'UpdatedLastName',
        }
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_profile_update_form_valid(self):
        """
        Test the profile update with valid data
        """
        with open(self.large_image_path, 'rb') as image_file:
            form_data = {'image': SimpleUploadedFile(
                name='sample-large.jpg',
                content=image_file.read(),
                content_type='image/jpeg')
            }
        form = ProfileUpdateForm(
            data={},
            files=form_data,
            instance=self.profile
        )
        self.assertTrue(form.is_valid())


class AuthenticationTest(TestCase):
    """
    Tests for the user authentication.
    This class focusing on the functionality and reliability of the
    login and logout processes.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the test case.
        """
        cls.user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='testpass123'
        )

    def test_login_success(self):
        """
        Tests so the user can log in.
        """
        response = self.client.post(
            reverse('login'),
            {'email': 'test@example.com', 'password': 'testpass123'}
        )
        self.assertRedirects(response, reverse('cards-home'))
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_failure(self):
        """
        Tests so the user cannot log in with the wrong credentials.
        """
        response = self.client.post(
            reverse('login'),
            {'email': 'test@example.com', 'password': 'wrongpassword'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue('_auth_user_id' not in self.client.session)

    def test_logout(self):
        """
        Tests so the user can log out.
        """
        self.client.login(username='test@example.com', password='testpass123')
        self.assertTrue('_auth_user_id' in self.client.session)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'logout.html')
        self.assertTrue('_auth_user_id' not in self.client.session)
