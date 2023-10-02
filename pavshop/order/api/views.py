from rest_framework import generics
from rest_framework import permissions
from order.models import BillingAddress, ShippingAddress
from .serializers import BillingAddressSerializer,  ShippingAddressSerializer
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from blog.api.pagination import CustomPagination
from drf_yasg.utils import swagger_auto_schema


class BillingAddressListCreateAPIView(generics.ListCreateAPIView):
    queryset = BillingAddress.objects.all()
    serializer_class = BillingAddressSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CustomPagination

    @swagger_auto_schema(tags=["Billing Address API"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Billing Address API"])
    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ShippingAddressListCreateAPIView(generics.ListCreateAPIView):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CustomPagination

    @swagger_auto_schema(tags=["Shipping Address API"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Shipping Address API"])
    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)