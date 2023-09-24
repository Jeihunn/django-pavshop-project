from django.urls import path
from . import views

app_name = "product"
urlpatterns = [
    path("products/", views.product_list_view, name="product_list_view"),
    path("product/<slug:product_slug>/",
         views.product_detail_view, name="product_detail_view"),
    path("wishlist/", views.wishlist_view, name="wishlist_view"),
    path("toggle-wishlist/", views.toggle_wishlist, name="toggle_wishlist"),
    path("remove-wishlist/", views.remove_from_wishlist,
         name="remove_from_wishlist"),
                         # # # Generic # # #
    #     path("products/", views.ProductListView.as_view(), name="product_list_view"),
    #     path("product/<slug:slug>/",
    #          views.ProductDetailView.as_view(), name="product_detail_view"),
]
