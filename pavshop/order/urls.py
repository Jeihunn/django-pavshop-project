from django.urls import path
from . import views

app_name = "order"
urlpatterns = [
    path("checkout/", views.checkout_view, name="checkout_view"),

    # Paypal
    path("payment-completed/", views.payment_completed_view, name="payment_completed"),
    path("payment-failed/", views.payment_failed_view, name="payment_failed"),
]
