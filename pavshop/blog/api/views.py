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
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .pagination import CustomPagination
from .filters import BlogFilter, BlogReviewFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


class BlogListAPIView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogListSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = BlogFilter
    search_fields = ["title"]


class BlogReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = BlogReview.objects.filter(parent=None)
    serializer_class = BlogReviewListSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = BlogReviewFilter
    search_fields = ["subject", "comment"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BlogReviewCreateSerializer
        return self.serializer_class


class BlogReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogReview.objects.all()
    serializer_class = BlogReviewDetailSerializer
    permission_classes = [IsOwnerOrSuperuserCanDeleteOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
