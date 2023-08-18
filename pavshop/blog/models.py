from django.db import models
from django.utils import timezone
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from core.models import AbstractModel
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.


class BlogCategory(AbstractModel):
    name = models.CharField(verbose_name=_("Name"), max_length=50, unique=True)
    is_active = models.BooleanField(verbose_name=_("Active"), default=True)
    slug = AutoSlugField(populate_from="name", unique=True)

    class Meta:
        verbose_name = _("Blog Category")
        verbose_name_plural = _("Blog Categories")

    def __str__(self):
        return self.name


class BlogTag(AbstractModel):
    name = models.CharField(verbose_name=_("Name"), max_length=50, unique=True)
    is_active = models.BooleanField(verbose_name=_("Active"), default=True)
    slug = AutoSlugField(populate_from="name", unique=True)

    class Meta:
        verbose_name = _("Blog Tag")
        verbose_name_plural = _("Blog Tags")

    def __str__(self):
        return self.name


class Blog(AbstractModel):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="blogs", verbose_name=_("Author"))
    blog_categories = models.ManyToManyField(
        BlogCategory, related_name="blogs", verbose_name=_("Blog Categories"))
    blog_tags = models.ManyToManyField(
        BlogTag, related_name="blogs", verbose_name=_("Blog Tags"))

    title = models.CharField(verbose_name=_("Title"), max_length=250)
    content = RichTextField(verbose_name=_("Content"))
    cover_image = models.ImageField(verbose_name=_(
        "Cover Image"), upload_to="blog_cover_images", default="blog_cover_images/default_blog_cover.jpg")
    publish_date = models.DateTimeField(
        verbose_name=_("Publish Date"), default=timezone.now)
    is_active = models.BooleanField(verbose_name=_("Active"), default=True)
    slug = AutoSlugField(populate_from="title", unique=True)

    class Meta:
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")

    def __str__(self):
        return f"{self.title} - ({self.author})"


class BlogReview(AbstractModel):
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="reviews", verbose_name=_("Blog"))
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children", verbose_name=_("Parent"))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="blog_reviews", verbose_name=_("User"))

    full_name = models.CharField(verbose_name=_(
        "Full Name"), max_length=150, null=True, blank=True)
    email = models.EmailField(verbose_name=_(
        "Email"), max_length=50, null=True, blank=True)
    subject = models.CharField(verbose_name=_("Subject"), max_length=100)
    comment = models.TextField(verbose_name=_("Comment"))

    class Meta:
        verbose_name = _("Blog Review")
        verbose_name_plural = _("Blog Reviews")

    def __str__(self):
        if self.user:
            user_identifier = self.user.get_username()
        else:
            user_identifier = self.full_name

        if self.parent:
            return f"{self.subject} - {user_identifier} ~~ (Parent: {self.parent})"
        else:
            return f"{self.subject} - {user_identifier}"
