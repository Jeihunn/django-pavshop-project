from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path("blogs/archive/<str:year>/<str:month>/", views.blog_archive_view, name='blog_archive_view'),
    path("blogs/category/<slug:category_slug>/", views.blog_category_view, name='blog_category_view'),
    path("blogs/tag/<slug:tag_slug>/", views.blog_tag_view, name='blog_tag_view'),
    path("blogs/search/", views.blog_search_view, name='blog_search_view'),
    path("blogs/", views.blog_list_view, name="blog_list_view"),
    path("blog/<slug:blog_slug>/", views.blog_detail_view, name="blog_detail_view"),
]
