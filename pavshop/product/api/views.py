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
    Wishlist,
    ShoppingCart
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
    WishlistCreateUpdateSerializer,
    ShoppingCartSerializer
)
from .permissions import IsSuperuserOrReadOnly
from blog.api.permissions import IsOwnerOrSuperuserCanDeleteOrReadOnly
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from blog.api.pagination import CustomPagination
from .filters import (
    ProductCategoryFilter,
    ProductTagFilter,
    ColorFilter,
    DesignerFilter,
    BrandFilter,
    ProductVersionFilter,
    WishlistFilter,
    ShoppingCartFilter
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from drf_yasg.utils import swagger_auto_schema


class ProductCategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsSuperuserOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = ProductCategoryFilter
    search_fields = ["name"]

    @swagger_auto_schema(tags=["Product Category API"])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Product Category API"])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProductCategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsSuperuserOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    @swagger_auto_schema(tags=["Product Category API"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Product Category API"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Product Category API"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Product Category API"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ProducTagListAPIView(generics.ListAPIView):
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = ProductTagFilter
    search_fields = ["name"]

    @swagger_auto_schema(tags=["Product Tag API"])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ColorListAPIView(generics.ListAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = ColorFilter
    search_fields = ["name"]

    @swagger_auto_schema(tags=["Color API"])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class DesignerListAPIView(generics.ListAPIView):
    queryset = Designer.objects.all()
    serializer_class = DesignerSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = DesignerFilter
    search_fields = ["name"]

    @swagger_auto_schema(tags=["Designer API"])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BrandListAPIView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = BrandFilter
    search_fields = ["name"]

    @swagger_auto_schema(tags=["Brand API"])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


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

    @swagger_auto_schema(tags=["Product API"])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Product API"])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [IsSuperuserOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return ProductCreateUpdateSerializer
        return self.serializer_class

    @swagger_auto_schema(tags=["Product API"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Product API"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Product API"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Product API"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ProductVersionListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProductVersion.objects.all()
    serializer_class = ProductVersionListSerializer
    permission_classes = [IsSuperuserOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = ProductVersionFilter
    search_fields = ["title"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductVersionCreateUpdateSerializer
        return self.serializer_class

    @swagger_auto_schema(tags=["Product Version API"])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Product Version API"])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProductVersionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductVersion.objects.all()
    serializer_class = ProductVersionListSerializer
    permission_classes = [IsSuperuserOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return ProductVersionCreateUpdateSerializer
        return self.serializer_class

    @swagger_auto_schema(tags=["Product Version API"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Product Version API"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Product Version API"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Product Version API"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


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

    @swagger_auto_schema(tags=["Wishlist API"])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Wishlist API"])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class WishlistDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistListSerializer
    permission_classes = [IsOwnerOrSuperuserCanDeleteOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return WishlistCreateUpdateSerializer
        return self.serializer_class

    @swagger_auto_schema(tags=["Wishlist API"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Wishlist API"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Wishlist API"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Wishlist API"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ShoppingCartListAPIView(generics.ListAPIView):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShoppingCartFilter

    @swagger_auto_schema(tags=["ShoppingCart API"])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)