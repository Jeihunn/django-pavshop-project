from django.db import models
from core.models import AbstractModel
from product.models import ProductVersion
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.


class BillingAddress(AbstractModel):
    first_name = models.CharField(verbose_name=_("First Name"), max_length=255)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=255)
    company_name = models.CharField(verbose_name=_("Company Name"), max_length=255, blank=True, null=True)
    address = models.CharField(verbose_name=_("Address"), max_length=255)
    city = models.CharField(verbose_name=_("City"), max_length=255)
    country = models.CharField(verbose_name=_("Country"), max_length=255)
    email = models.EmailField(verbose_name=_("Email"), max_length=255)
    phone_number = PhoneNumberField(verbose_name=_("Phone Number"))

    class Meta:
        verbose_name = _("Billing Address")
        verbose_name_plural = _("Billing Addresses")

    def __str__(self):
        return f"Billing Address for {self.first_name} {self.last_name} - {self.id}"


class ShippingAddress(AbstractModel):
    first_name = models.CharField(verbose_name=_("First Name"), max_length=255)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=255)
    company_name = models.CharField(verbose_name=_("Company Name"), max_length=255, blank=True, null=True)
    address = models.CharField(verbose_name=_("Address"), max_length=255)
    city = models.CharField(verbose_name=_("City"), max_length=255)
    country = models.CharField(verbose_name=_("Country"), max_length=255)
    email = models.EmailField(verbose_name=_("Email"), max_length=255)
    phone_number = PhoneNumberField(verbose_name=_("Phone Number"))

    class Meta:
        verbose_name = _("Shipping Address")
        verbose_name_plural = _("Shipping Addresses")

    def __str__(self):
        return f"Shipping Address for {self.first_name} {self.last_name} - {self.id}"


class Order(AbstractModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders", verbose_name=_("User"))
    billing_address = models.ForeignKey(
        BillingAddress, on_delete=models.SET_NULL, null=True, related_name="orders", verbose_name=_("Billing Address"))
    shipping_address = models.ForeignKey(
        ShippingAddress, on_delete=models.SET_NULL, null=True, related_name="orders", verbose_name=_("Shipping Address"))
    
    ordered_date = models.DateTimeField(verbose_name=_("Ordered Date"), auto_now_add=True)
    is_paid = models.BooleanField(verbose_name=_("Paid"), default=False)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(AbstractModel):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items", verbose_name=_("Order"))
    product_version = models.ForeignKey(
        ProductVersion, on_delete=models.CASCADE, related_name="order_items", verbose_name=_("Product Version"))
    
    quantity = models.PositiveIntegerField(
        verbose_name=_("Quantity"), default=1)
    price = models.DecimalField(
        verbose_name=_("Price"), max_digits=10, decimal_places=2)
    
    @property
    def total_price(self):
        return self.quantity * self.price

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    def __str__(self):
        return f"Order Item #{self.id}"