from django.db import models
from core.models import AbstractModel
from autoslug import AutoSlugField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.


class Color(AbstractModel):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(verbose_name="Active", default=True)

    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colors"

    def __str__(self):
        return self.name


class Designer(AbstractModel):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(verbose_name="Active", default=True)

    class Meta:
        verbose_name = "Designer"
        verbose_name_plural = "Designers"

    def __str__(self):
        return self.name


class Brand(AbstractModel):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(verbose_name="Active", default=True)
    slug = AutoSlugField(populate_from="name", unique=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name


class Discount(AbstractModel):
    name = models.CharField(max_length=30, unique=True)
    percent = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(verbose_name="Active", default=True)

    class Meta:
        verbose_name = "Discount"
        verbose_name_plural = "Discounts"

    def __str__(self):
        return f"{self.name} - ({self.percent}%)"


class ProductCategory(AbstractModel):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(verbose_name="Active", default=True)
    slug = AutoSlugField(populate_from="name", unique=True)

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return self.name


class ProductTag(AbstractModel):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(verbose_name="Active", default=True)
    slug = AutoSlugField(populate_from="name", unique=True)

    class Meta:
        verbose_name = "Product Tag"
        verbose_name_plural = "Product Tags"

    def __str__(self):
        return self.name


class Product(AbstractModel):
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    product_category = models.ManyToManyField(ProductCategory)
    product_tag = models.ManyToManyField(ProductTag)

    title = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from="title", unique=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.title


class ProductVersion(AbstractModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    designer = models.ForeignKey(
        Designer, on_delete=models.SET_NULL, null=True)
    color = models.ManyToManyField(Color)
    discount = models.ForeignKey(
        Discount, on_delete=models.SET_NULL, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)
    cover_image = models.ImageField(
        upload_to="product_cover_images", default="product_cover_images/default_product_cover.jpg")
    is_active = models.BooleanField(verbose_name="Active", default=True)

    class Meta:
        verbose_name = "Product Version"
        verbose_name_plural = "Product Versions"

    def __str__(self):
        return f"{self.product.title} - {self.designer.name} - {self.price}$"


class ProductVersionImage(AbstractModel):
    product_version = models.ForeignKey(
        ProductVersion, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="product_images", default="product_images/default_product.jpg")
    is_active = models.BooleanField(verbose_name="Active", default=True)

    class Meta:
        verbose_name = "Product Version Image"
        verbose_name_plural = "Product Version Images"

    def __str__(self):
        return str(self.image)


class ProductVersionReview(AbstractModel):
    product_version = models.ForeignKey(
        ProductVersion, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    full_name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    comment = models.TextField()

    class Meta:
        verbose_name = "Product Version Review"
        verbose_name_plural = "Product Version Reviews"

    def __str__(self):
        if len(self.comment) > 30:
            return f"{self.comment[:30]}..."
        else:
            return self.comment


class Wishlist(AbstractModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product_version = models.ManyToManyField(ProductVersion)

    class Meta:
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"

    def __str__(self):
        return self.user.username
