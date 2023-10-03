from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase
from blog.models import Blog, BlogReview
from core.models import Newsletter
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your tests here.


class BlogApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpassword")
        self.blog = Blog.objects.create(
            author=self.user,
            title="Test Blog",
            content="Test content",
            is_active=True,
        )

    def test_api_blog_list_url(self):
        url = reverse_lazy("api_blog:api_blog_list_view")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_blog_review_list_create_url(self):
        url = reverse_lazy("api_blog:api_blog_review_list_create_view")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_blog_review_detail_url(self):
        blog_review = BlogReview.objects.create(
            blog=self.blog,
            user=self.user,
            subject="Test Subject",
            comment="Test Comment",
        )

        url = reverse_lazy("api_blog:api_blog_review_detail_view", kwargs={"pk": blog_review.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class NewsletterAPITest(APITestCase):
    def setUp(self):
        self.test_email = "test@example.com"
        self.test_subscription_status = True

    def test_create_newsletter(self):
        url = reverse_lazy("api_core:api_newsletter_create_view")
        data = {
            "email": self.test_email,
            "subscription_status": self.test_subscription_status,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        newsletter = Newsletter.objects.get(email=self.test_email)
        self.assertEqual(newsletter.subscription_status, self.test_subscription_status)
