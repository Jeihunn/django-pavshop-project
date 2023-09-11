from rest_framework import generics
from rest_framework import permissions
from product.models import (
    ProductCategory,
    ProductTag,
    Color,
    Designer,
    Brand,
    Product,
    ProductVersion,
    Wishlist
)
from .serializers import (
    ProductCategorySerializer,
    ProductTagSerializer,
    ColorSerializer,
    DesignerSerializer,
    BrandSerializer,
    ProductListSerializer,
    ProductCreateUpdateSerializer,
    ProductVersionListSerializer,
    ProductVersionCreateUpdateSerializer,
    WishlistListSerializer,
    WishlistCreateUpdateSerializer
)
from .permissions import IsSuperuserOrReadOnly
from blog.api.permissions import IsOwnerOrSuperuserCanDeleteOrReadOnly
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from blog.api.pagination import CustomPagination
from .filters import ProductCategoryFilter, ProductTagFilter, WishlistFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


class ProductCategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsSuperuserOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = ProductCategoryFilter
    search_fields = ["name"]


class ProductCategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsSuperuserOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


class ProducTagListAPIView(generics.ListAPIView):
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = ProductTagFilter
    search_fields = ["name"]


class ColorListAPIView(generics.ListAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class DesignerListAPIView(generics.ListAPIView):
    queryset = Designer.objects.all()
    serializer_class = DesignerSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class BrandListAPIView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [IsSuperuserOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter]
    search_fields = ["title"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductCreateUpdateSerializer
        return self.serializer_class


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [IsSuperuserOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return ProductCreateUpdateSerializer
        return self.serializer_class


class ProductVersionListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProductVersion.objects.all()
    serializer_class = ProductVersionListSerializer
    permission_classes = [IsSuperuserOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductVersionCreateUpdateSerializer
        return self.serializer_class


class ProductVersionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductVersion.objects.all()
    serializer_class = ProductVersionListSerializer
    permission_classes = [IsSuperuserOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return ProductVersionCreateUpdateSerializer
        return self.serializer_class


class WishlistListCreateAPIView(generics.ListCreateAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = WishlistFilter

    def get_serializer_class(self):
        if self.request.method == "POST":
            return WishlistCreateUpdateSerializer
        return self.serializer_class


class WishlistDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistListSerializer
    permission_classes = [IsOwnerOrSuperuserCanDeleteOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return WishlistCreateUpdateSerializer
        return self.serializer_class
