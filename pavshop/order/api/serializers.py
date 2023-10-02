from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from order.models import ShippingAddress, BillingAddress


class BillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingAddress
        fields = (
            "id",
            "first_name",
            "last_name",
            "company_name",
            "address",
            "city",
            "country",
            "email",
            "phone_number",
        )


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = (
            "id",
            "first_name",
            "last_name",
            "company_name",
            "address",
            "city",
            "country",
            "email",
            "phone_number",
        )