from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path('blog-list/', views.blog_list_view, name="blog_list_view"),
    path('blog-detail/', views.blog_detail_view, name="blog_detail_view"),
]
