from django.shortcuts import render

# Create your views here.

def index_view(request):
    return render(request, "core/index.html")


def contact_view(request):
    return render(request, "core/contact.html")


def checkout_view(request):
    return render(request, "core/checkout.html")


def about_us_view(request):
    return render(request, "core/about-us.html")