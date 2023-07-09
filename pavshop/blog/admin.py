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
    pass


@admin.register(BlogReview)
class BlogReviewAdmin(admin.ModelAdmin):
    form = BlogReviewAdminForm
