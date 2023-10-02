from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from colorfield.fields import ColorField
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


# Create your models here.


COLOR_PALETTE = (
        ("#000000", "Black"),
        ("#FFFFFF", "White"),
        ("#FF0000", "Red"),
        ("#0000FF", "Blue"),
        ("#00FF00", "Green"),
        ("#FFFF00", "Yellow"),
        ("#800080", "Purple"),
        ("#008080", "Teal"),
    )


class AbstractModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name=_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name=_("Updated At"), auto_now=True)

    class Meta:
        abstract = True


class Contact(AbstractModel):
    full_name = models.CharField(verbose_name=_("Full Name"), max_length=150)
    email = models.EmailField(verbose_name=_("Email"), max_length=50)
    phone_number = PhoneNumberField(verbose_name=_("Phone Number"))
    subject = models.CharField(verbose_name=_("Subject"), max_length=100)
    message = models.TextField(verbose_name=_("Message"))

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

    def __str__(self):
        return f"{self.subject} - {self.full_name}"


class Newsletter(AbstractModel):
    email = models.EmailField(verbose_name=_(
        "Email"), max_length=50, unique=True)
    subscription_status = models.BooleanField(
        verbose_name=_("Subscription Status"), default=True)

    class Meta:
        verbose_name = _("Newsletter")
        verbose_name_plural = _("Newsletters")

    def __str__(self):
        return self.email


class SubBanner(AbstractModel):
    PAGE_CHOICES = (
        ("all_pages", _("All Pages")),
        ("core:about_us_view", _("About Us Page")),
        ("core:contact_view", _("Contact Page")),
        ("product:wishlist_view", _("Wishlist Page")),
        ("login_view", _("Login Page")),
        ("register_view", _("Register Page")),
        ("blog:blog_list_view", _("Blog List Page")),
        ("blog:blog_detail_view", _("Blog Detail Page")),
        ("product:product_list_view", _("Product List Page")),
        ("product:product_detail_view", _("Product Detail Page")),
        ("product:shopping_cart_view", _("Shopping Cart Page")),
        ("product:checkout_view", _("Checkout Page")),
    )

    page = models.CharField(verbose_name=_(
        "Page"), max_length=250, unique=True, choices=PAGE_CHOICES)
    title = models.CharField(verbose_name=_(
        "Title"), max_length=100, blank=True, null=True)
    title_color = ColorField(verbose_name=_(
        "Title Color"), format="hexa", samples=COLOR_PALETTE, blank=True, null=True)
    title_font_size = models.PositiveIntegerField(verbose_name=_(
        "Title Font Size"), blank=True, null=True)
    description = models.TextField(verbose_name=_(
        "Description"), blank=True, null=True)
    description_color = ColorField(verbose_name=_(
        "Description Color"), format="hexa", samples=COLOR_PALETTE, blank=True, null=True)
    description_font_size = models.PositiveIntegerField(verbose_name=_(
        "Description Font Size"), blank=True, null=True)
    breadcrumbs = models.CharField(verbose_name=_(
        "Breadcrumbs"), max_length=255, blank=True, null=True)
    image = models.ImageField(verbose_name=_("Image"), upload_to="sub_banners")
    is_active = models.BooleanField(verbose_name=_("Active"), default=True)

    class Meta:
        verbose_name = _("Sub Banner")
        verbose_name_plural = _("Sub Banners")

    def __str__(self):
        return f"{self.page} - {self.title}"
    

from product.models import ProductVersion

class ReklamBanner(AbstractModel):
    product_version = models.ForeignKey(
        ProductVersion, on_delete=models.CASCADE, null=True, blank=True, related_name="reklam_banners", verbose_name=_("Product Version"))
    
    name = models.CharField(verbose_name=_("Name"), max_length=100)
    title = models.CharField(verbose_name=_("Title"), max_length=100, blank=True, null=True)
    title_color = ColorField(verbose_name=_("Title Color"), format="hex", samples=COLOR_PALETTE, blank=True, null=True)
    title_font_size = models.PositiveIntegerField(verbose_name=_("Title Font Size"), blank=True, null=True)
    link = models.URLField(verbose_name=_("Link"), max_length=255, blank=True, null=True)
    image = models.ImageField(verbose_name=_("Image"), upload_to="reklam_banners", blank=True, null=True)
    is_active = models.BooleanField(verbose_name=_("Active"), default=True)

    def clean(self):
        if self.product_version:
            if ReklamBanner.objects.filter(product_version=self.product_version).exclude(id=self.id).exists():
                raise ValidationError({
                    "product_version": _("An advertisement already exists for this product version."),
                })
            if self.image or self.link:
                raise ValidationError({
                    "image": _("If a product version is selected, image must be empty."),
                    "link": _("If a product version is selected, link must be empty."),
                })
        else:
            if not self.image:
                raise ValidationError({
                    "image": _("If no product version is selected, the image must be provided."),
                })

    class Meta:
        verbose_name = _("Reklam Banner")
        verbose_name_plural = _("Reklam Banners")

    def __str__(self):
        return f"{self.id} - reklam banner"