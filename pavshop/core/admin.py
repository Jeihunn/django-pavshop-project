from django.contrib import admin
from .models import Contact, Newsletter, SubBanner, ReklamBanner
from .forms import SubBannerAdminForm
from django.contrib.admin.models import LogEntry
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.admin.widgets import AdminTextInputWidget
from modeltranslation.admin import TranslationAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html


# Register your models here.


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["id", "subject", "full_name", "email",
                    "phone_number", "created_at", "updated_at"]
    list_display_links = ["id", "subject"]
    list_filter = ["created_at"]
    search_fields = ["subject", "full_name", "email", "phone_number"]

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'phone_number':
            kwargs['widget'] = PhoneNumberPrefixWidget(
                attrs={'class': 'vTextField'})
            kwargs['widget'].widget = AdminTextInputWidget(
                attrs={'class': 'vTextField'})
        return super().formfield_for_dbfield(db_field, **kwargs)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "subscription_status",
                    "created_at", "updated_at"]
    list_display_links = ["id", "email"]
    list_editable = ["subscription_status"]
    list_filter = ["subscription_status", "created_at", "updated_at"]
    search_fields = ["email"]


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ["action_time", "user", "content_type",
                    "object_id", "object_repr", "action_flag"]
    list_filter = ["action_time", "user", "action_flag"]


@admin.register(SubBanner)
class SubBannerAdmin(TranslationAdmin):
    form = SubBannerAdminForm

    list_display = ["id", "page", "image_thumbnail", "breadcrumbs_display", "is_active", "title", "colored_title_color", "title_font_size_px", "description",
                    "colored_description_color", "description_font_size_px"]
    list_display_links = ["id", "page"]
    list_editable = ["is_active"]

    def colored_title_color(self, obj):
        if obj.title_color:
            return format_html('<div style="background-color:{}; width:30px; height:30px; border:1px solid #000; border-radius:50%;"></div>', obj.title_color)
        return None
    colored_title_color.admin_order_field = "title_color"
    colored_title_color.short_description = _("Title Color")

    def title_font_size_px(self, obj):
        if obj.title_font_size:
            return f"{obj.title_font_size}px"
        return None
    title_font_size_px.admin_order_field = "title_font_size"
    title_font_size_px.short_description = _("Title Font Size (px)")

    def colored_description_color(self, obj):
        if obj.description_color:
            return format_html(
                '<div style="background-color:{}; width:30px; height:30px; border:1px solid #000; border-radius:50%;"></div>', obj.description_color)
        return None
    colored_description_color.admin_order_field = "description_color"
    colored_description_color.short_description = _("Description Color")

    def description_font_size_px(self, obj):
        if obj.description_font_size:
            return f"{obj.description_font_size}px"
        return None
    description_font_size_px.admin_order_field = "description_font_size"
    description_font_size_px.short_description = _(
        "Description Font Size (px)")

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" class="thumbnail-image" />', obj.image.url)
        return None
    image_thumbnail.short_description = _("Image")

    def breadcrumbs_display(self, obj):
        if obj.breadcrumbs:
            breadcrumbs_list = obj.breadcrumbs.split(" > ")
            breadcrumbs_html = "<span style='color: #FF0000; font-weight: bold;'> &gt; </span>".join(
                [format_html('<span style="color: #fff; background-color: #007BFF; padding: 0 5px; border-radius: 7px;">{}</span>',
                             breadcrumb) for breadcrumb in breadcrumbs_list]
            )
            return format_html(breadcrumbs_html)
        return None
    breadcrumbs_display.short_description = _("Breadcrumbs")

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css', 'admin_custom.css'),
            'all': ('css/admin_custom.css',),
        }


@admin.register(ReklamBanner)
class ReklamBannerAdmin(TranslationAdmin):
    fields = ["name", "product_version", "title", "title_color",
              "title_font_size", "link", "image", "is_active"]
    raw_id_fields = ["product_version"]

    list_display = ["id", "name", "product_version", "is_product_version_active", "title", "colored_title_color",
                    "title_font_size_px", "image_thumbnail", "is_active", "link"]
    list_display_links = ["id", "name"]
    list_editable = ["is_active"]
    search_fields = ["name"]

    def is_product_version_active(self, obj):
        if obj.product_version:
            return obj.product_version.is_active
        return None
    is_product_version_active.boolean = True
    is_product_version_active.admin_order_field = "product_version__is_active"
    is_product_version_active.short_description = _("Product Version Active")

    def colored_title_color(self, obj):
        if obj.title_color:
            return format_html('<div style="background-color:{}; width:30px; height:30px; border:1px solid #000; border-radius:50%;"></div>', obj.title_color)
        return None
    colored_title_color.admin_order_field = "title_color"
    colored_title_color.short_description = _("Title Color")

    def title_font_size_px(self, obj):
        if obj.title_font_size:
            return f"{obj.title_font_size}px"
        return None
    title_font_size_px.admin_order_field = "title_font_size"
    title_font_size_px.short_description = _("Title Font Size (px)")

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" class="thumbnail-image" />', obj.image.url)
        return None
    image_thumbnail.short_description = _("Image")

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css', 'admin_custom.css'),
            'all': ('css/admin_custom.css',),
        }
