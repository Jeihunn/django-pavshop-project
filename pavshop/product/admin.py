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


# Inline
class ProductVersionImageInline(admin.TabularInline):
    model = ProductVersionImage
    extra = 1
# END Inline


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
    pass


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
    inlines = [ProductVersionImageInline]


@admin.register(ProductVersionImage)
class ProductVersionImageAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductVersionReview)
class ProductVersionReviewAdmin(admin.ModelAdmin):
    form = ProductVersionReviewAdminForm


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    pass
