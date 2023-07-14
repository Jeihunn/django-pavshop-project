from django.urls import path
from . import views

app_name = "core"
urlpatterns = [
    path('', views.index_view, name="index_view"),
    path('shopping-cart/', views.shopping_cart_view, name="shopping_cart_view"),
    path('wishlist/', views.wishlist_view, name="wishlist_view"),
    path('contact/', views.contact_view, name="contact_view"),
    path('checkout/', views.checkout_view, name="checkout_view"),
    path('about-us/', views.about_us_view, name="about_us_view"),
]
