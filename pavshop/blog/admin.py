from django.contrib import admin
from .models import BlogCategory, BlogTag, Blog, BlogReview
from .forms import BlogReviewAdminForm

# Register your models here.


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    pass


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ["title", "slug"]


@admin.register(BlogReview)
class BlogReviewAdmin(admin.ModelAdmin):
    form = BlogReviewAdminForm

    list_display = ["id", "subject", "user", "full_name",
                    "email", "blog", "created_at", "updated_at",]
    list_display_links = ["id", "subject"]
