from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import ContactForm


# Create your views here.


def index_view(request):
    return render(request, "core/index.html")


def shopping_cart_view(request):
    return render(request, "core/shopping-cart.html")


def wishlist_view(request):
    return render(request, "core/wishlist.html")


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank You. Your message has been sent successfully!")
            return redirect(reverse_lazy("core:contact_view"))
        else:
            messages.error(request, "Oops! Something went wrong. Please review your message and make sure all the required fields are filled correctly.")
    else:
        form = ContactForm()

    context = {
        "form": form,
    }
    return render(request, "core/contact.html", context)


def checkout_view(request):
    return render(request, "core/checkout.html")


def about_us_view(request):
    return render(request, "core/about-us.html")
