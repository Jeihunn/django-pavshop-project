from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from .models import ProductVersion, Wishlist
from .forms import ProductVersionReviewForm


# Create your views here.


def product_list_view(request):
    return render(request, "product/product-list.html")


def product_detail_view(request, product_slug):
    product_version = get_object_or_404(
        ProductVersion, slug=product_slug, is_active=True)

    comments = product_version.reviews.order_by("-created_at")
    related_product_versions = ProductVersion.objects.filter(
        product__product_categories__in=product_version.product.product_categories.all()
    ).exclude(id=product_version.id).filter(is_active=True).distinct()[:15]

    if request.method == "POST":
        form = ProductVersionReviewForm(data=request.POST, user=request.user)
        if form.is_valid():
            review = form.save(commit=False)
            review.product_version = product_version
            if request.user.is_authenticated:
                review.user = request.user
            form.save()
            messages.success(request, _(
                "Your comment has been successfully saved."))
            return redirect(reverse_lazy("product:product_detail_view", kwargs={"product_slug": product_slug}))
        else:
            messages.error(request, _(
                "There was an error saving your comment. Please review the fields and make sure they are correct."))
    else:
        form = ProductVersionReviewForm(user=request.user)

    context = {
        "product_version": product_version,
        "form": form,
        "comments": comments,
        "related_product_versions": related_product_versions
    }
    return render(request, "product/product-detail.html", context)


@login_required(login_url=reverse_lazy("login_view"))
def wishlist_view(request):
    try:
        wishlist = request.user.wishlist
    except Wishlist.DoesNotExist:
        wishlist = None

    if wishlist:
        product_versions = wishlist.product_versions.filter(is_active=True)
    else:
        product_versions = []

    context = {
        "product_versions": product_versions,
    }
    return render(request, "product/wishlist.html", context)


@login_required(login_url=reverse_lazy("login_view"))
def toggle_wishlist(request):
    product_version_id = request.GET.get("product_version_id")
    try:
        product_version = ProductVersion.objects.get(id=product_version_id)
    except ProductVersion.DoesNotExist:
        return JsonResponse({"error": "Product version not found."}, status=400)

    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    if product_version in wishlist.product_versions.all():
        wishlist.remove_product(product_version)
        is_added = False
    else:
        wishlist.add_product(product_version)
        is_added = True

    response_data = {
        "is_added": is_added,
        "wishlist_count": wishlist.product_versions.filter(is_active=True).count()
    }
    return JsonResponse(response_data)


@login_required(login_url=reverse_lazy("login_view"))
def remove_from_wishlist(request):
    product_version_id = request.GET.get("product_version_id")
    try:
        product_version = ProductVersion.objects.get(id=product_version_id)
    except ProductVersion.DoesNotExist:
        return JsonResponse({"error": "Product version not found."}, status=400)

    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.remove_product(product_version)

    response_data = {
        "success": True,
        "wishlist_count": wishlist.product_versions.filter(is_active=True).count()
    }
    return JsonResponse(response_data)


# Generic

class ProductListView(TemplateView):
    template_name = "product/product-list.html"


class ProductDetailView(DetailView):
    model = ProductVersion
    template_name = "product/product-detail.html"
    context_object_name = "product_version"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product_version = context['product_version']
        context['comments'] = product_version.reviews.order_by("-created_at")
        context['related_product_versions'] = ProductVersion.objects.filter(
            product__product_categories__in=product_version.product.product_categories.all()
        ).exclude(id=product_version.id).filter(is_active=True).distinct()[:15]

        if self.request.method == "POST":
            form = ProductVersionReviewForm(
                data=self.request.POST, user=self.request.user)
            if form.is_valid():
                review = form.save(commit=False)
                review.product_version = product_version
                if self.request.user.is_authenticated:
                    review.user = self.request.user
                form.save()
                messages.success(self.request, _(
                    "Your comment has been successfully saved."))
                return redirect(reverse_lazy(
                    "product:product_detail_view",
                    kwargs={"product_slug": product_version.slug}))
            else:
                messages.error(
                    self.request, _('''There was an error saving your comment. 
                    Please review the fields and make sure they are correct.'''))
        else:
            form = ProductVersionReviewForm(user=self.request.user)

        context['form'] = form
        return context
