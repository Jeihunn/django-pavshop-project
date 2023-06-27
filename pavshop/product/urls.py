from django.urls import path
from . import views

app_name = "product"
urlpatterns = [
    path('product-list/', views.product_list_view, name="product_list_view"),
    path('product-detail/', views.product_detail_view, name="product_detail_view"),
]
