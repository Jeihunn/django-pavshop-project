import django_filters
from django import forms
from blog.models import Blog, BlogReview


class BlogFilter(django_filters.FilterSet):
    author__id = django_filters.NumberFilter(
        field_name="author__id",
        lookup_expr="exact",
        label="Author ID",
        widget=forms.NumberInput(
            attrs={"placeholder": "Search by author id"}),
    )

    publish_date__gte = django_filters.DateFilter(
        field_name="publish_date",
        lookup_expr="gte",
        label="Publish Date is greater than or equal to (YYYY-MM-DD):",
        widget=forms.DateInput(
            attrs={"type": "date", "placeholder": "YYYY-MM-DD"},
        )
    )

    publish_date__lte = django_filters.DateFilter(
        field_name="publish_date",
        lookup_expr="lte",
        label="Publish Date is less than (YYYY-MM-DD):",
        widget=forms.DateInput(
            attrs={"type": "date", "placeholder": "YYYY-MM-DD"},
        )
    )

    is_active = django_filters.BooleanFilter(
        field_name="is_active",
        label="Blog Active",
    )

    order_by = django_filters.OrderingFilter(
        fields=(
            ("id", "id"),
            ("publish_date", "publish_date"),
            ("title", "title"),
        ),
        field_labels={
            "id": "id",
            "publish_date": "publish_date",
            "title": "title",
        },
    )

    class Meta:
        model = Blog
        fields = ["author__id", "publish_date__gte",
                  "publish_date__lte", "is_active", "order_by"]


class BlogReviewFilter(django_filters.FilterSet):
    user__id = django_filters.NumberFilter(
        field_name="user__id", lookup_expr="exact",
        label="User ID",
        widget=forms.NumberInput(
            attrs={"placeholder": "Search by user id"}
        )
    )

    blog__id = django_filters.NumberFilter(
        field_name="blog__id", lookup_expr="exact",
        label="Blog ID",
        widget=forms.NumberInput(
            attrs={"placeholder": "Search by blog id"}
        )
    )

    order_by = django_filters.OrderingFilter(
        fields=(
            ("id", "id"),
            ("created_at", "created_at"),
            ("updated_at", "updated_at"),
        ),
        field_labels={
            "id": "id",
            "created_at": "created_at",
            "updated_at": "updated_at",
        },
    )

    class Meta:
        model = BlogReview
        fields = ["user__id", "blog__id", "order_by"]
