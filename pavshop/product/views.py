from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from .models import ProductVersion
from .forms import ProductVersionReviewForm


# Create your views here.


def product_list_view(request):
    return render(request, "product/product-list.html")


def product_detail_view(request):
    if request.method == "POST":
        form = ProductVersionReviewForm(data=request.POST, user=request.user)
        if form.is_valid():
            review = form.save(commit=False)
            review.product_version = ProductVersion.objects.first()  # bu hissə dəyişəcək və aktiv ProductVersion olacaq
            if request.user.is_authenticated:
                review.user = request.user
            form.save()
            messages.success(request, "Your comment has been successfully saved.")
            return redirect(reverse_lazy("product:product_detail_view"))
        else:
            messages.error(request, "There was an error saving your comment. Please review the fields and make sure they are correct.")
    else:
        form = ProductVersionReviewForm(user=request.user)

    context = {
        "form": form,
    }
    return render(request, "product/product-detail.html", context)
