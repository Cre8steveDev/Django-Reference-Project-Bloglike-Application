from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Post


class PostTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="reader",
            email="reader@example.com",
            password="test-password",
            name="Test Reader",
        )

    def test_post_slug_is_generated_when_post_is_created(self):
        post = Post.objects.create(
            author=self.user,
            title="A useful note",
            category="field-notes",
            body="A short note worth returning to.",
        )

        self.assertTrue(post.slug.startswith("a-useful-note-"))
        self.assertEqual(
            post.get_absolute_url(),
            reverse("post-detail", args=[post.slug]),
        )

    def test_authenticated_user_can_publish_a_post(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("create-post"),
            {
                "title": "A published note",
                "category": "reading-list",
                "body": "This note was created through the post form.",
            },
        )

        post = Post.objects.get(title="A published note")
        self.assertRedirects(response, post.get_absolute_url())
        self.assertEqual(post.author, self.user)
