from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from .models import Blog


# Create your views here.


def blog_list_view(request):
    blogs = Blog.objects.filter(is_active=True).order_by("-publish_date")

    paginator = Paginator(blogs, 6)
    page = request.GET.get('page')
    try:
        page_number = int(page)
    except TypeError:
        page_number = 1
    except ValueError:
        raise Http404("Invalid page number.")

    try:
        blogs = paginator.page(page_number)
    except EmptyPage:
        raise Http404("Invalid page number.")

    context = {
        "blogs": blogs,
    }
    return render(request, "blog/blog-list.html", context)


def blog_detail_view(request, blog_slug):
    blog = get_object_or_404(Blog, slug=blog_slug, is_active=True)

    related_blogs = Blog.objects.filter(
        Q(blog_categories__in=blog.blog_categories.all()) & ~Q(id=blog.id)).distinct()[:3]

    if "recently_viewed" in request.session:
        if blog.id in request.session["recently_viewed"]:
            request.session["recently_viewed"].remove(blog.id)

        request.session["recently_viewed"].insert(0, blog.id)
        if len(request.session["recently_viewed"]) > 5:
            request.session["recently_viewed"].pop()
    else:
        request.session["recently_viewed"] = [blog.id]
    request.session.modified = True

    context = {
        "blog": blog,
        "related_blogs": related_blogs,
    }
    return render(request, "blog/blog-detail.html", context)


def blog_archive_view(request, year, month):
    month = month.lower()

    try:
        blog_date = datetime.strptime(f"{year}/{month}", "%Y/%B")
    except ValueError:
        raise Http404("Invalid date format.")

    blogs = Blog.objects.filter(is_active=True, publish_date__year=year,
                                publish_date__month=blog_date.month).order_by("-publish_date")

    paginator = Paginator(blogs, 6)
    page = request.GET.get('page')
    try:
        page_number = int(page)
    except TypeError:
        page_number = 1
    except ValueError:
        raise Http404("Invalid page number.")

    try:
        blogs = paginator.page(page_number)
    except EmptyPage:
        raise Http404("Invalid page number.")

    context = {
        "blogs": blogs,
    }
    return render(request, "blog/blog-list.html", context)
