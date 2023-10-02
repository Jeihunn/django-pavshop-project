from django.urls import path
from . import views as api_views

app_name = "api_order"
urlpatterns = [
    path("billing-address/", api_views.BillingAddressListCreateAPIView.as_view(),
         name="api_billing_address_list_create_view"),
    path("shipping-address/", api_views.ShippingAddressListCreateAPIView.as_view(),
         name="api_shipping_address_list_create_view"),
]
