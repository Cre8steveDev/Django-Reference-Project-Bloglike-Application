from django.contrib.auth.models import AbstractUser
from django.db import models

GENDER = [("Male", "Male"), ("Female", "Female"), ("Other", "Other")]


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "name"]

    name = models.CharField(max_length=255)
    birthday = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/%Y/%m/", null=True, blank=True)
    gender = models.CharField(choices=GENDER, null=True, blank=True, max_length=10)
    portfolio_url = models.URLField(blank=True)

    def __str__(self):
        return self.name
