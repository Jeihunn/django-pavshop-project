from django import template
from django.db.models import Case, When, IntegerField
from django.db.models import Count
from blog.models import Blog, BlogTag, BlogCategory

register = template.Library()


@register.inclusion_tag('blog/includes/recent-post.html')
def get_recently_viewed_blogs(request):
    if "recently_viewed" in request.session:
        blog_ids = request.session["recently_viewed"]
        blog_id_positions = {blog_id: index for index,
                             blog_id in enumerate(blog_ids)}
        case_ordering = Case(*[When(pk=blog_id, then=index) for blog_id,
                             index in blog_id_positions.items()], output_field=IntegerField())
        recently_viewed_blogs = Blog.objects.filter(
            pk__in=blog_ids, is_active=True).order_by(case_ordering)
        return {"recently_viewed_blogs": recently_viewed_blogs}
    return {"recently_viewed_blogs": None}


@register.inclusion_tag('blog/includes/blog-popular-tags.html')
def get_blog_popular_tags(limit=10):
    tag_count = BlogTag.objects.filter(
        is_active=True).annotate(blog_count=Count('blogs'))
    blog_popular_tags = tag_count.order_by('-blog_count')[:limit]
    return {'blog_popular_tags': blog_popular_tags}


@register.simple_tag
def get_blog_categories(limit=20):
    return BlogCategory.objects.filter(is_active=True)[:limit]
