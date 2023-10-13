from django.db import models
from core.models import AbstractModel, CustomImageField, COLOR_PALETTE
from autoslug import AutoSlugField
from colorfield.fields import ColorField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.


class Color(AbstractModel):
    name = models.CharField(verbose_name=_(
        "Color Name"), max_length=50, unique=True)
    hex_code = ColorField(verbose_name=_("Hex Code"),
                          format="hex", unique=True, samples=COLOR_PALETTE)
    is_active = models.BooleanField(verbose_name=_("Active"), default=True)

    class Meta:
        verbose_name = _("Color")
        verbose_name_plural = _("Colors")

    def __str__(self):
        return self.name


class Designer(AbstractModel):
    name = models.CharField(verbose_name=_("Designer"),
                            max_length=50, unique=True)
    is_active = models.BooleanField(verbose_name=_("Active"), default=True)

    class Meta:
        verbose_name = _("Designer")
        verbose_name_plural = _("Designers")

    def __str__(self):
        return self.name


class Brand(AbstractModel):
    name = models.CharField(verbose_name=_(
        "Brand"), max_length=50, unique=True)
    is_active = models.BooleanField(verbose_name=_("Active"), default=True)
    slug = AutoSlugField(verbose_name=_("Brand"),
                         populate_from="name", unique=True)

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        return self.name


class Discount(AbstractModel):
    products = models.ManyToManyField(
        "ProductVersion", blank=True, related_name="discounts", verbose_name=_("Products"))

    name = models.CharField(verbose_name=_("Name"), max_length=50, unique=True)
    percent = models.PositiveSmallIntegerField(verbose_name=_(
        "Percent"), validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(verbose_name=_("Active"), default=True)

    class Meta:
        verbose_name = _("Discount")
        verbose_name_plural = _("Discounts")

    def __str__(self):
        return f"{self.name} - ({self.percent}%)"


class ProductCategory(AbstractModel):
    name = models.CharField(verbose_name=_("Name"), max_length=50, unique=True)
    is_active = models.BooleanField(verbose_name=_("Active"), default=True)
    slug = AutoSlugField(populate_from="name", unique=True)

    class Meta:
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")

    @property
    def product_count(self):
        count = 0
        for product in self.products.all():
            for product_version in product.versions.filter(is_active=True):
                count += 1
        return count

    def __str__(self):
        return self.name


class ProductTag(AbstractModel):
    name = models.CharField(verbose_name=_("Name"), max_length=50, unique=True)
    is_active = models.BooleanField(verbose_name=_("Active"), default=True)
    slug = AutoSlugField(populate_from="name", unique=True)

    class Meta:
        verbose_name = _("Product Tag")
        verbose_name_plural = _("Product Tags")

    @property
    def product_count(self):
        count = 0
        for product in self.products.all():
            for product_version in product.versions.filter(is_active=True):
                count += 1
        return count

    def __str__(self):
        return self.name


class Product(AbstractModel):
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, null=True, related_name="products", verbose_name=_("Brand"))
    product_categories = models.ManyToManyField(
        ProductCategory, related_name="products", verbose_name=_("Product Categories"))
    product_tags = models.ManyToManyField(
        ProductTag, related_name="products", verbose_name=_("Product Tags"))

    title = models.CharField(verbose_name=_("Title"), max_length=250)
    slug = AutoSlugField(populate_from="title", unique=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.title


class ProductVersion(AbstractModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="versions", verbose_name=_("Product"))
    designer = models.ForeignKey(
        Designer, on_delete=models.SET_NULL, null=True, related_name="product_versions", verbose_name=_("Designer"))
    colors = models.ManyToManyField(
        Color, related_name="product_versions", verbose_name=_("Colors"))

    title = models.CharField(verbose_name=_("Title"), max_length=250)
    price = models.DecimalField(verbose_name=_(
        "Price"), max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"))
    description = models.TextField(verbose_name=_(
        "Description"), null=True, blank=True)
    cover_image = CustomImageField(verbose_name=_(
        "Cover Image"), upload_to="product_cover_images", default="product_cover_images/default_product_cover.jpg")
    is_active = models.BooleanField(verbose_name=_("Active"), default=True)
    slug = AutoSlugField(populate_from="title", unique=True)

    @property
    def total_discount(self):
        total_discount = 0
        for discount in self.discounts.all():
            total_discount += discount.percent
        return total_discount

    @property
    def discounted_price(self):
        return self.price - (self.price * self.total_discount / 100)

    class Meta:
        verbose_name = _("Product Version")
        verbose_name_plural = _("Product Versions")

    def __str__(self):
        return f"Product: {self.product.title} - Version: {self.title} - Designer: {self.designer.name} - Price: {self.price}$"


class ProductVersionImage(AbstractModel):
    product_version = models.ForeignKey(
        ProductVersion, on_delete=models.CASCADE, related_name="images", verbose_name=_("Product Version"))

    image = CustomImageField(verbose_name=_(
        "Image"), upload_to="product_images", default="product_images/default_product.jpg")
    is_active = models.BooleanField(verbose_name=_("Active"), default=True)

    class Meta:
        verbose_name = _("Product Version Image")
        verbose_name_plural = _("Product Version Images")

    def __str__(self):
        return str(self.image)


class ProductVersionReview(AbstractModel):
    product_version = models.ForeignKey(
        ProductVersion, on_delete=models.CASCADE, related_name="reviews", verbose_name=_("Product Version"))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="product_reviews", verbose_name=_("User"))

    full_name = models.CharField(verbose_name=_(
        "Full Name"), max_length=150, null=True, blank=True)
    email = models.EmailField(verbose_name=_(
        "Email"), max_length=50, null=True, blank=True)
    comment = models.TextField(verbose_name=_("Comment"))

    class Meta:
        verbose_name = _("Product Version Review")
        verbose_name_plural = _("Product Version Reviews")

    def __str__(self):
        if self.user:
            user_identifier = self.user.get_username()
        else:
            user_identifier = self.full_name

        if len(self.comment) > 30:
            truncated_comment = self.comment[:30] + "..."
        else:
            truncated_comment = self.comment

        return f"{user_identifier} - {truncated_comment}"


class Wishlist(AbstractModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="wishlist", verbose_name=_("User"))
    product_versions = models.ManyToManyField(
        ProductVersion, blank=True, related_name="wishlists", verbose_name=_("Product Versions"))

    def add_product(self, product_version):
        if not self.product_versions.filter(pk=product_version.pk).exists():
            self.product_versions.add(product_version)

    def remove_product(self, product_version):
        self.product_versions.remove(product_version)

    class Meta:
        verbose_name = _("Wishlist")
        verbose_name_plural = _("Wishlists")

    def __str__(self):
        return self.user.username


class ShoppingCart(AbstractModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="shopping_cart", verbose_name=_("User"))
    products = models.ManyToManyField(
        ProductVersion, through="CartItem", related_name="carts")

    @property
    def total_price(self):
        total_price = 0
        for item in self.items.filter(product_version__is_active=True):
            total_price += item.product_version.discounted_price * item.quantity
        return total_price

    class Meta:
        verbose_name = _("Shopping Cart")
        verbose_name_plural = _("Shopping Carts")

    def __str__(self):
        return f"Shopping Cart for {self.user.username}"


class CartItem(AbstractModel):
    cart = models.ForeignKey(
        ShoppingCart, on_delete=models.CASCADE, related_name="items", verbose_name=_("Cart"))
    product_version = models.ForeignKey(
        ProductVersion, on_delete=models.CASCADE, related_name="cart_items", verbose_name=_("Product Version"))

    quantity = models.PositiveIntegerField(
        verbose_name=_("Quantity"), default=1)

    @property
    def total_price(self):
        return self.quantity * self.product_version.discounted_price

    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")

    def __str__(self):
        return f"{self.quantity} x {self.product_version.title} in Cart"
