from django.shortcuts import render

# Create your views here.


def blog_list_view(request):
    return render(request, "blog/blog-list.html")


def blog_detail_view(request):
    return render(request, "blog/blog-detail.html")
