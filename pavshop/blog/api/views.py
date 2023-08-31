from rest_framework import generics
from rest_framework import permissions
from blog.models import Blog, BlogReview
from .serializers import (
    BlogListSerializer,
    BlogReviewListSerializer,
    BlogReviewCreateSerializer,
    BlogReviewDetailSerializer,
)
from .permissions import IsOwnerOrSuperuserCanDeleteOrReadOnly
from .pagination import CustomPagination
from .filters import BlogFilter, BlogReviewFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class BlogListAPIView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = BlogFilter
    search_fields = ["title"]
    ordering_fields = ["id", "publish_date", "title"]


class BlogReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = BlogReview.objects.filter(parent=None)
    serializer_class = BlogReviewListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = BlogReviewFilter
    search_fields = ["subject", "comment"]
    ordering_fields = ["id", "created_at", "updated_at"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BlogReviewCreateSerializer
        return self.serializer_class


class BlogReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogReview.objects.all()
    serializer_class = BlogReviewDetailSerializer
    permission_classes = [IsOwnerOrSuperuserCanDeleteOrReadOnly]
