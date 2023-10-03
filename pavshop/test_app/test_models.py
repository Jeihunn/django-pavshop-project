from django.test import TestCase
from blog.models import Blog, BlogCategory, BlogTag, BlogReview
from core.models import Contact, Newsletter
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your tests here.


class BlogModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword")

        self.category = BlogCategory.objects.create(
            name="Test Category", is_active=True)

        self.tag = BlogTag.objects.create(name="Test Tag", is_active=True)

        self.blog = Blog.objects.create(
            author=self.user,
            title="Test Blog",
            content="This is a test blog content.",
            cover_image="blog_cover_images/test_image.jpg",
            is_active=True,
        )
        self.blog.blog_categories.add(self.category)
        self.blog.blog_tags.add(self.tag)

        self.review = BlogReview.objects.create(
            blog=self.blog,
            user=self.user,
            subject="Test Review",
            comment="This is a test review comment.",
        )

    def test_blog_model(self):
        self.assertEqual(self.blog.title, "Test Blog")
        self.assertEqual(self.blog.author, self.user)
        self.assertEqual(self.blog.blog_categories.count(), 1)
        self.assertEqual(self.blog.blog_tags.count(), 1)
        self.assertTrue(self.blog.is_active)

    def test_blog_review_model(self):
        self.assertEqual(self.review.subject, "Test Review")
        self.assertEqual(self.review.comment, "This is a test review comment.")
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.blog, self.blog)

    def test_blog_category_model(self):
        self.assertEqual(self.category.name, "Test Category")
        self.assertTrue(self.category.is_active)

    def test_blog_tag_model(self):
        self.assertEqual(self.tag.name, "Test Tag")
        self.assertTrue(self.tag.is_active)


class CoreModelsTestCase(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            full_name="John Doe",
            email="john@example.com",
            phone_number="1234567890",
            subject="Test Subject",
            message="Test Message",
        )

        self.newsletter = Newsletter.objects.create(
            email="test@example.com",
            subscription_status=True,
        )

    def test_contact_model(self):
        self.assertEqual(str(self.contact), "Test Subject - John Doe")

    def test_newsletter_model(self):
        self.assertEqual(str(self.newsletter), "test@example.com")
