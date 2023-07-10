from django.db import models
from django.utils import timezone
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from smart_selects.db_fields import ChainedForeignKey
from core.models import AbstractModel
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.


class BlogCategory(AbstractModel):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(verbose_name="Active", default=True)
    slug = AutoSlugField(populate_from="name", unique=True)

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"

    def __str__(self):
        return self.name


class BlogTag(AbstractModel):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(verbose_name="Active", default=True)
    slug = AutoSlugField(populate_from="name", unique=True)

    class Meta:
        verbose_name = "Blog Tag"
        verbose_name_plural = "Blog Tags"

    def __str__(self):
        return self.name


class Blog(AbstractModel):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="blogs")
    blog_categories = models.ManyToManyField(
        BlogCategory, related_name="blogs")
    blog_tags = models.ManyToManyField(BlogTag, related_name="blogs")

    title = models.CharField(max_length=250)
    content = RichTextField()
    cover_image = models.ImageField(
        upload_to="blog_cover_images", default="blog_cover_images/default_blog_cover.jpg")
    publish_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(verbose_name="Active", default=True)
    slug = AutoSlugField(populate_from="title", unique=True)

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

    def __str__(self):
        return f"{self.title} - ({self.author})"


class BlogReview(AbstractModel):
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="reviews")
    parent = ChainedForeignKey(
        "self",
        chained_field="blog",
        chained_model_field="blog",
        show_all=False,
        auto_choose=False,
        sort=True,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="blog_reviews")

    full_name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    subject = models.CharField(max_length=100)
    comment = models.TextField()

    class Meta:
        verbose_name = "Blog Review"
        verbose_name_plural = "Blog Reviews"

    def __str__(self):
        if self.user:
            user_identifier = self.user.get_username()
        else:
            user_identifier = self.full_name

        if self.parent:
            return f"{self.subject} - {user_identifier} ~~ (Parent: {self.parent})"
        else:
            return f"{self.subject} - {user_identifier}"
