from django.views.generic import ListView, DetailView
from datetime import datetime
from django.shortcuts import render, get_object_or_404, Http404
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from .models import Blog, BlogCategory, BlogTag


# Create your views here.


def blog_list_view(request):
    category_slug = request.GET.get("category")
    tag_slug = request.GET.get("tag")
    query = request.GET.get("query")

    blogs = Blog.objects.filter(is_active=True).order_by("-publish_date")

    category = None
    tag = None

    if category_slug:
        category = get_object_or_404(
            BlogCategory, slug=category_slug, is_active=True)
        blogs = blogs.filter(blog_categories__slug=category_slug)

    if tag_slug:
        tag = get_object_or_404(BlogTag, slug=tag_slug, is_active=True)
        blogs = blogs.filter(blog_tags__slug=tag_slug)

    if query:
        # blogs = blogs.filter(title__icontains=query) # Hər dilin yalnız özünə uyğun axtarış etmək üçün.
        # Həm AZ, həm də EN title field-lərində axtarış etmək üçün.
        blogs = blogs.filter(Q(title_az__icontains=query)
                             | Q(title_en__icontains=query))

    blogs_count = blogs.count()

    paginator = Paginator(blogs, 6)
    page = request.GET.get("page")
    try:
        page_number = int(page)
    except TypeError:
        page_number = 1
    except ValueError:
        raise Http404(_("Invalid page number."))

    try:
        blogs = paginator.page(page_number)
    except EmptyPage:
        raise Http404(_("Invalid page number."))

    context = {
        "blogs": blogs,
        "blogs_count": blogs_count,
        "selected_category": category,
        "selected_tag": tag,
        "selected_query": query,
    }
    return render(request, "blog/blog-list.html", context)


def blog_detail_view(request, blog_slug):
    blog = get_object_or_404(Blog, slug=blog_slug, is_active=True)

    comments = blog.reviews.filter(parent=None).order_by("-created_at")
    related_blogs = Blog.objects.filter(
        Q(blog_categories__in=blog.blog_categories.all()) & ~Q(id=blog.id)).filter(
            is_active=True).distinct()[:3]

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
        "comments": comments,
    }
    return render(request, "blog/blog-detail.html", context)


def blog_archive_view(request, year, month):
    month = month.lower()

    try:
        blog_date = datetime.strptime(f"{year}/{month}", "%Y/%B")
    except ValueError:
        raise Http404(_("Invalid date format."))

    blogs = Blog.objects.filter(is_active=True, publish_date__year=year,
                                publish_date__month=blog_date.month).order_by("-publish_date")
    blogs_count = blogs.count()

    paginator = Paginator(blogs, 6)
    page = request.GET.get("page")
    try:
        page_number = int(page)
    except TypeError:
        page_number = 1
    except ValueError:
        raise Http404(_("Invalid page number."))

    try:
        blogs = paginator.page(page_number)
    except EmptyPage:
        raise Http404(_("Invalid page number."))

    context = {
        "blogs": blogs,
        "blogs_count": blogs_count,
    }
    return render(request, "blog/blog-list.html", context)


# ===== Generic Views =====

class BlogListView(ListView):
    template_name = "blog/blog-list.html"
    model = Blog
    context_object_name = "blogs"
    paginate_by = 6

    def get_queryset(self):
        category_slug = self.request.GET.get("category")
        tag_slug = self.request.GET.get("tag")
        query = self.request.GET.get("query")

        blogs = Blog.objects.filter(is_active=True).order_by("-publish_date")

        if category_slug:
            blogs = blogs.filter(blog_categories__slug=category_slug)

        if tag_slug:
            blogs = blogs.filter(blog_tags__slug=tag_slug)

        if query:
            blogs = blogs.filter(Q(title_az__icontains=query)
                                 | Q(title_en__icontains=query))

        return blogs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blogs_count"] = self.get_queryset().count()
        context["selected_category"] = self.request.GET.get("category")
        context["selected_tag"] = self.request.GET.get("tag")
        context["selected_query"] = self.request.GET.get("query")
        return context


class BlogDetailView(DetailView):
    template_name = "blog/blog-detail.html"
    model = Blog
    context_object_name = "blog"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = context["blog"]
        context["related_blogs"] = Blog.objects.filter(
            Q(blog_categories__in=blog.blog_categories.all()) & ~Q(id=blog.id)
        ).filter(is_active=True).distinct()[:3]
        context["comments"] = blog.reviews.filter(
            parent=None).order_by("-created_at")
        return context


class BlogArchiveView(ListView):
    template_name = "blog/blog-list.html"
    model = Blog
    context_object_name = "blogs"
    paginate_by = 6

    def get_queryset(self):
        year = self.kwargs.get("year")
        month = self.kwargs.get("month").lower()

        try:
            blog_date = datetime.strptime(f"{year}/{month}", "%Y/%B")
        except ValueError:
            raise Http404(_("Invalid date format."))

        blogs = Blog.objects.filter(
            is_active=True,
            publish_date__year=year,
            publish_date__month=blog_date.month
        ).order_by("-publish_date")

        return blogs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blogs_count"] = self.get_queryset().count()
        return context
