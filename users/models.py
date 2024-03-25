from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import os


class Profile(models.Model):
    """
    Extends the default Django User model to include a profile image.

    Attributes:
        user (User): The user associated with this profile.
        image (ImageField): The profile image for the user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        """
        Return a string representation of the user profile.
        """
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        """
        Override the save method to resize the uploaded profile image to a
        maximum dimension of 300x300px before saving it and converting it to
        webp format.
        """
        img = Image.open(self.image)

        # Resize the image if it's bigger than 300px
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)

            in_mem_file = BytesIO()
            img.save(in_mem_file, format='webp')
            in_mem_file.seek(0)

            filename = os.path.basename(self.image.name)
            self.image.save(
                filename,
                ContentFile(in_mem_file.read()),
                save=False
            )

            in_mem_file.close()

        super().save(*args, **kwargs)
