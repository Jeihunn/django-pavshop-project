from django.contrib import admin
from .models import BlogCategory, BlogTag, Blog, BlogReview
from .forms import BlogReviewAdminForm


# Register your models here.


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "is_active",
                    "slug", "created_at", "updated_at"]
    list_display_links = ["id", "name"]
    list_editable = ["is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "is_active",
                    "slug", "created_at", "updated_at"]
    list_display_links = ["id", "name"]
    list_editable = ["is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    filter_horizontal = ["blog_categories", "blog_tags"]

    list_display = ["id", "title", "is_active",
                    "publish_date", "get_categories", "get_tags", "author", "created_at", "updated_at"]
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
    get_categories.short_description = "Categories"

    def get_tags(self, obj):
        arr = []
        for tag in obj.blog_tags.all():
            arr.append(tag)
        return arr
    get_tags.short_description = "Tags"


@admin.register(BlogReview)
class BlogReviewAdmin(admin.ModelAdmin):
    form = BlogReviewAdminForm

    list_display = ["id", "subject", "parent",
                    "get_blog_title", "user", "full_name", "email"]
    list_display_links = ["id", "subject"]
    list_filter = ["blog", "user"]

    def get_blog_title(self, obj):
        return obj.blog.title
    get_blog_title.admin_order_field = "blog"
    get_blog_title.short_description = "Blog"
