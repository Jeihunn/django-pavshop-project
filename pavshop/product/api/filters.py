import django_filters
from django import forms
from product.models import ProductCategory, ProductTag, Wishlist


class ProductCategoryFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(
        field_name="is_active",
        label="Product Category Active",
    )

    order_by = django_filters.OrderingFilter(
        fields=(
            ("id", "id"),
            ("created_at", "created_at"),
            ("name", "name"),
        ),
        field_labels={
            "id": "id",
            "created_at": "created_at",
            "name": "name",
        },
    )

    class Meta:
        model = ProductCategory
        fields = ["is_active", "order_by"]


class ProductTagFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(
        field_name="is_active",
        label="Product Category Active",
    )

    order_by = django_filters.OrderingFilter(
        fields=(
            ("id", "id"),
            ("created_at", "created_at"),
            ("name", "name"),
        ),
        field_labels={
            "id": "id",
            "created_at": "created_at",
            "name": "name",
        },
    )

    class Meta:
        model = ProductTag
        fields = ["is_active", "order_by"]


class WishlistFilter(django_filters.FilterSet):
    user__id = django_filters.NumberFilter(
        field_name="user__id",
        lookup_expr="exact",
        label="User ID",
        widget=forms.NumberInput(
            attrs={"placeholder": "Search by user id"}),
    )

    class Meta:
        model = Wishlist
        fields = ["user__id"]
