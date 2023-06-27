from django.urls import path
from . import views

app_name = "core"
urlpatterns = [
    path('', views.index_view, name="index_view"),
    path('cart', views.cart_view, name="cart_view"),
    
]