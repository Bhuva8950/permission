from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class MyUser(AbstractUser):

    is_allow = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.email}"


