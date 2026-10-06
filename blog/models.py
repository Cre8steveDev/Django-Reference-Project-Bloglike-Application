import random

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Post(models.Model):
    CATEGORY_CHOICES = [
        ("field-notes", "Field notes"),
        ("reading-list", "Reading list"),
        ("small-rituals", "Small rituals"),
        ("on-making", "On making"),
        ("city-walks", "City walks"),
        ("kitchen-notes", "Kitchen notes"),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    body = models.TextField()
    cover_image = models.ImageField(upload_to="posts/%Y/%m/", blank=True, null=True)
    reading_time = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "post"
            characters = "abcdefghijklmnopqrstuvwxyz0123456789"
            suffix = "".join(random.choices(characters, k=4))
            self.slug = f"{base_slug}-{suffix}"

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"post_slug": self.slug})

    @property
    def excerpt(self):
        if len(self.body) <= 180:
            return self.body
        return f"{self.body[:177].rstrip()}..."
