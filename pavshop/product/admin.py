from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.contrib import messages
from modeltranslation.admin import TranslationAdmin
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
    Wishlist,
    ShoppingCart,
    CartItem,
)


# Register your models here.


# ========== Inline ==========
class DiscountInline(admin.TabularInline):
    model = Discount.products.through
    extra = 1
    verbose_name = _("Discount")
    verbose_name_plural = _("Discounts")


class ProductVersionImageInline(admin.TabularInline):
    model = ProductVersionImage
    extra = 1
    verbose_name = _("Image")
    verbose_name_plural = _("Images")


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    verbose_name = _("Cart Item")
    verbose_name_plural = _("Cart Items")
# ========== END Inline ==========


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "hex_code", "colored_hex_code", "is_active", "created_at", "updated_at"]
    list_display_links = ["id", "name"]
    list_editable = ["is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]

    def colored_hex_code(self, obj):
        if obj.hex_code:
            return format_html('<div style="background-color:{}; width:30px; height:30px; border:1px solid #000; border-radius:50%;"></div>', obj.hex_code)
        return None
    colored_hex_code.admin_order_field = "hex_code"
    colored_hex_code.short_description = _("Color")


@admin.register(Designer)
class DesignerAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "is_active", "created_at", "updated_at"]
    list_display_links = ["id", "name"]
    list_editable = ["is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "is_active", "created_at", "updated_at"]
    list_display_links = ["id", "name"]
    list_editable = ["is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    fields = ["name", "percent", "is_active", "products"]
    filter_horizontal = ["products"]

    list_display = ["id", "name", "get_percent",
                    "is_active", "created_at", "updated_at"]
    list_display_links = ["id", "name"]
    list_editable = ["is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]

    def get_percent(self, obj):
        return f"{obj.percent}%"
    get_percent.admin_order_field = "percent"
    get_percent.short_description = _("Percent")


@admin.register(ProductCategory)
class ProductCategoryAdmin(TranslationAdmin):
    list_display = ["id", "name", "is_active",
                    "slug", "created_at", "updated_at"]
    list_display_links = ["id", "name"]
    list_editable = ["is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "is_active",
                    "slug", "created_at", "updated_at"]
    list_display_links = ["id", "name"]
    list_editable = ["is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    filter_horizontal = ["product_categories", "product_tags"]

    list_display = ["id", "title", "brand", "get_categories",
                    "get_tags", "slug", "created_at", "updated_at"]
    list_display_links = ["id", "title"]
    list_filter = ["brand", "product_categories", "product_tags"]
    search_fields = ["title", "brand"]

    def get_categories(self, obj):
        arr = []
        for category in obj.product_categories.all():
            arr.append(category)
        return arr
    get_categories.short_description = _("Categories")

    def get_tags(self, obj):
        arr = []
        for tag in obj.product_tags.all():
            arr.append(tag)
        return arr
    get_tags.short_description = _("Tags")

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(ProductVersion)
class ProductVersionAdmin(TranslationAdmin):
    inlines = [DiscountInline, ProductVersionImageInline]
    filter_horizontal = ["colors"]
    actions = ["action_clear_discounts"]

    list_display = ["id", "title", "cover_image_thumbnail", "designer", "product", "price", "quantity",
                    "is_active", "get_colors", "get_discounts", "slug", "created_at", "updated_at"]
    list_display_links = ["id", "title"]
    list_filter = ["is_active", "product",
                   "colors", "created_at", "updated_at"]
    search_fields = ["title"]

    def get_colors(self, obj):
        arr = []
        for color in obj.colors.all():
            arr.append(color)
        return arr
    get_colors.short_description = _("Colors")

    def get_discounts(self, obj):
        arr = []
        for discount in obj.discounts.all():
            arr.append(f"{discount.percent}%")
        return arr
    get_discounts.short_description = _("Discounts")

    def cover_image_thumbnail(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" class="thumbnail-image" />', obj.cover_image.url)
        return None
    cover_image_thumbnail.short_description = _("Cover Image")

    def action_clear_discounts(modeladmin, request, queryset):
        num_selected_products = queryset.count()
        
        for product_version in queryset:
            product_version.discounts.clear()
        
        if num_selected_products > 0:
            message = _("{} selected product(s) have had their discounts cleared.".format(num_selected_products))
            modeladmin.message_user(request, message, level=messages.SUCCESS)
    action_clear_discounts.short_description = _("Clear selected discounts")

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
            'all': ('css/admin_custom.css',),
        }


@admin.register(ProductVersionImage)
class ProductVersionImageAdmin(admin.ModelAdmin):
    list_display = ["id", "product_version", "is_active",
                    "image_thumbnail", "created_at", "updated_at"]
    list_display_links = ["id", "product_version"]
    list_filter = ["is_active", "product_version"]

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" class="thumbnail-image" />', obj.image.url)
        return None
    image_thumbnail.short_description = _("Image")

    class Media:
        css = {
            'all': ('css/admin_custom.css',),
        }



@admin.register(ProductVersionReview)
class ProductVersionReviewAdmin(admin.ModelAdmin):
    form = ProductVersionReviewAdminForm

    list_display = ["id", "product_version", "user",
                    "full_name", "email", "created_at", "updated_at"]
    list_display_links = ["id", "product_version"]
    list_filter = ["product_version", "user", "created_at", "updated_at"]
    search_fields = ["user__username", "user__first_name",
                     "user__last_name", "full_name", "email"]


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    filter_horizontal = ["product_versions"]

    list_display = ["user", "created_at", "updated_at"]
    search_fields = ["user__username"]


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ["user"]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["id", "cart", "product_version",
                    "is_product_version_active", "quantity"]
    raw_id_fields = ["product_version"]

    def is_product_version_active(self, obj):
        return obj.product_version.is_active
    is_product_version_active.boolean = True
    is_product_version_active.admin_order_field = "product_version__is_active"
    is_product_version_active.short_description = _(
        "Product Version is Active")
