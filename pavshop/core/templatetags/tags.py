import calendar
from django import template
from datetime import timedelta, date
from django.db.models import Case, When, IntegerField
from django.db.models import Count
from django.urls import reverse
from blog.models import Blog, BlogTag, BlogCategory

register = template.Library()


# ===== Filter =====
@register.filter(name='get_range')
def get_range(value: int) -> range:
    return range(value)
# ===== END Filter =====


# ===== Simple Tag =====
@register.simple_tag
def get_blog_categories(limit=20):
    return BlogCategory.objects.filter(is_active=True)[:limit]
# ===== END Simple Tag =====


# ===== Inclusion Tag =====
@register.inclusion_tag('blog/includes/recent-post.html', takes_context=True)
def get_recently_viewed_blogs(context):
    request = context['request']

    if 'recently_viewed' in request.session:
        blog_ids = request.session['recently_viewed']
        blog_id_positions = {blog_id: index for index,
                             blog_id in enumerate(blog_ids)}
        case_ordering = Case(*[When(pk=blog_id, then=index) for blog_id,
                             index in blog_id_positions.items()], output_field=IntegerField())
        recently_viewed_blogs = Blog.objects.filter(
            pk__in=blog_ids, is_active=True).order_by(case_ordering)
        return {
            'recently_viewed_blogs': recently_viewed_blogs,
            'request': request
        }
    return {
        'recently_viewed_blogs': None,
        'request': request
    }


@register.inclusion_tag('blog/includes/blog-popular-tags.html', takes_context=True)
def get_blog_popular_tags(context, limit=10):
    request = context['request']

    try:
        selected_tag = context['selected_tag']
    except KeyError:
        selected_tag = None

    tag_count = BlogTag.objects.filter(
        is_active=True).annotate(blog_count=Count('blogs'))
    blog_popular_tags = tag_count.order_by('-blog_count')[:limit]
    return {
        'blog_popular_tags': blog_popular_tags,
        'request': request,
        'selected_tag': selected_tag
    }


@register.inclusion_tag('blog/includes/previous-months.html', takes_context=True)
def get_previous_months(context, limit=6):
    request = context['request']

    today = date.today()
    previous_months = []

    for i in range(limit):
        # Get the month and year
        month = today.strftime("%B")
        year = today.year

        # Create the URL
        path = reverse('blog:blog_archive_view', args=[year, month.lower()])

        previous_months.append({'month': month, 'year': year, 'path': path})

        # Calculate the last day of the previous month
        _, last_day = calendar.monthrange(year, today.month)
        today -= timedelta(days=last_day)

    return {
        'previous_months': previous_months,
        'request': request
    }
# ===== END Inclusion Tag =====
