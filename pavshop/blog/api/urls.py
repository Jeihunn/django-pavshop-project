from django.urls import path
from . import views as api_views

app_name = "api_blog"
urlpatterns = [
    path("blogs/", api_views.BlogListAPIView.as_view(), name="api_blog_list_view"),
    path("blog-reviews/", api_views.BlogReviewListCreateAPIView.as_view(),
         name="api_blog_review_list_create_view"),
    path("blog-review/<int:pk>/", api_views.BlogReviewDetailAPIView.as_view(),
         name="api_blog_review_detail_view"),
]
