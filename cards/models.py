from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name