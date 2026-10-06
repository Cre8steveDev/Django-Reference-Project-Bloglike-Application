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

    def test_create_page_requires_authentication(self):
        response = self.client.get(reverse("create-post"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('create-post')}",
        )

    def test_post_detail_page_renders_post_content(self):
        post = Post.objects.create(
            author=self.user,
            title="A detail page note",
            category="city-walks",
            body="The detail page should show this content.",
        )

        response = self.client.get(post.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A detail page note")
        self.assertContains(response, "The detail page should show this content.")
