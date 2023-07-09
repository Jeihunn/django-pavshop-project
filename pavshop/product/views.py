from django.shortcuts import render

# Create your views here.


def product_list_view(request):
    return render(request, "product/product-list.html")


def product_detail_view(request):
    return render(request, "product/product-detail.html")
