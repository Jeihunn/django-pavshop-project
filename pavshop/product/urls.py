from django.urls import path
from . import views

app_name = "product"
urlpatterns = [
    path("products/", views.product_list_view, name="product_list_view"),
    path("product/<slug:product_slug>/",
         views.product_detail_view, name="product_detail_view"),

    # Wishlist
    path("wishlist/", views.wishlist_view, name="wishlist_view"),
    path("toggle-wishlist/", views.toggle_wishlist, name="toggle_wishlist"),
    path("remove-wishlist/", views.remove_from_wishlist,
         name="remove_from_wishlist"),

    # Basket
    path("shopping-cart/", views.shopping_cart_view, name="shopping_cart_view"),
    path("remove-from-cart/", views.remove_from_cart, name="remove_from_cart"),
    path("add-to-cart/", views.add_to_cart, name="add_to_cart"),
    path("change-quantity/", views.select_change_quantity, name="select_change_quantity"),

    path("checkout/", views.checkout_view, name="checkout_view"),

    # # # Generic # # #
    #     path("products/", views.ProductListView.as_view(), name="product_list_view"),
    #     path("product/<slug:slug>/",
    #          views.ProductDetailView.as_view(), name="product_detail_view"),
]
