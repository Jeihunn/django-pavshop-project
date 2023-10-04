from django.contrib import admin
from .models import BlogCategory, BlogTag, Blog, BlogReview
from .forms import BlogReviewAdminForm
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin


# Register your models here.


@admin.register(BlogCategory)
class BlogCategoryAdmin(TranslationAdmin):
    list_display = ["id", "name", "is_active", "slug", "created_at", "updated_at"]
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


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "is_active",
                    "slug", "created_at", "updated_at"]
    list_display_links = ["id", "name"]
    list_editable = ["is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]


@admin.register(Blog)
class BlogAdmin(TranslationAdmin):
    filter_horizontal = ["blog_categories", "blog_tags"]

    list_display = ["id", "title", "cover_image_thumbnail", "is_active", "publish_date", "get_categories", "get_tags", "author", "created_at", "updated_at"]
    list_display_links = ["id", "title"]
    list_editable = ["is_active"]
    list_filter = ["is_active", "publish_date",
                   "author", "blog_categories", "blog_tags"]
    search_fields = ["title", "content"]

    def get_categories(self, obj):
        arr = []
        for category in obj.blog_categories.all():
            arr.append(category)
        return arr
    get_categories.short_description = _("Categories")

    def get_tags(self, obj):
        arr = []
        for tag in obj.blog_tags.all():
            arr.append(tag)
        return arr
    get_tags.short_description = _("Tags")

    def cover_image_thumbnail(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" class="thumbnail-image" />', obj.cover_image.url)
        return None
    cover_image_thumbnail.short_description = _("Cover Image")

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


@admin.register(BlogReview)
class BlogReviewAdmin(admin.ModelAdmin):
    form = BlogReviewAdminForm

    list_display = ["id", "subject", "parent", "get_blog_id", "get_blog_title",
                    "user", "full_name", "email", "created_at", "updated_at"]
    list_display_links = ["id", "subject"]
    list_filter = ["blog", "user"]
    raw_id_fields = ["blog", "parent"]

    def get_blog_id(self, obj):
        return obj.blog.id
    get_blog_id.admin_order_field = "blog"
    get_blog_id.short_description = _("Blog ID")

    def get_blog_title(self, obj):
        return obj.blog.title
    get_blog_title.admin_order_field = "blog"
    get_blog_title.short_description = _("Blog Title")
