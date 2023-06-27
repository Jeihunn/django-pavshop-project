from django.urls import path
from . import views

app_name = "core"
urlpatterns = [
    path('', views.index_view, name="index_view"),
    path('cart', views.cart_view, name="cart_view"),
    path('contact/', views.contact_view, name="contact_view"),
    path('checkout/', views.checkout_view, name="checkout_view"),
    path('about-us/', views.about_us_view, name="about_us_view"),
]