from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import os


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
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
