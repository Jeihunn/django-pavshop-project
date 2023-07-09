from django.contrib import admin
from .forms import ProductVersionReviewAdminForm
from .models import (
    Color,
    Designer,
    Brand,
    Discount,
    ProductCategory,
    ProductTag,
    Product,
    ProductVersion,
    ProductVersionImage,
    ProductVersionReview,
    Wishlist
)


# Register your models here.


# ========== Inline ==========
class DiscountInline(admin.TabularInline):
    model = Discount.products.through
    extra = 1
    verbose_name = "Discount"
    verbose_name_plural = "Discounts"


class ProductVersionImageInline(admin.TabularInline):
    model = ProductVersionImage
    extra = 1
    verbose_name = "Image"
    verbose_name_plural = "Images"
# ========== END Inline ==========


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    pass


@admin.register(Designer)
class DesignerAdmin(admin.ModelAdmin):
    pass


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    fields = ["name", "percent", "is_active", "products"]
    filter_horizontal = ["products"]


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductVersion)
class ProductVersionAdmin(admin.ModelAdmin):
    inlines = [DiscountInline, ProductVersionImageInline]


@admin.register(ProductVersionImage)
class ProductVersionImageAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductVersionReview)
class ProductVersionReviewAdmin(admin.ModelAdmin):
    form = ProductVersionReviewAdminForm


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    filter_horizontal = ["product_versions"]
