from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from product.models import ShoppingCart
from paypal.standard.forms import PayPalPaymentsForm


# Create your views here.


@login_required(login_url=reverse_lazy("login_view"))
@csrf_exempt
def payment_completed_view(request):
    return render(request, "order/payment-completed.html")


@login_required(login_url=reverse_lazy("login_view"))
@csrf_exempt
def payment_failed_view(request):
    return render(request, "order/payment-failed.html")


@login_required(login_url=reverse_lazy("login_view"))
def checkout_view(request):
    cart = ShoppingCart.objects.filter(user=request.user).first()

    host = request.get_host()
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": cart.total_price,
        "item_name": "Order",
        "invoice": "INVOICE-0001",
        "currency_code": "USD",
        "notify_url": "http://" + host + reverse_lazy("paypal-ipn"),
        "return_url": "http://" + host + reverse_lazy("order:payment_completed"),
        "cancel_return": "http://" + host + reverse_lazy("order:payment_failed"),
    }

    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

    context = {
        "cart": cart,
        "paypal_payment_button": paypal_payment_button,
    }
    return render(request, "order/checkout.html", context)
