import django_filters
from django import forms
from blog.models import Blog, BlogReview


class BlogFilter(django_filters.FilterSet):
    author_id = django_filters.CharFilter(
        field_name="author__id", lookup_expr="exact",
        label="Author ID",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by author id"}),
    )

    publish_date = django_filters.DateFromToRangeFilter(
        field_name="publish_date",
        label="Publish Date Range (YYYY-MM-DD)",
        widget=django_filters.widgets.RangeWidget(
            attrs={"type": "date", "placeholder": "YYYY-MM-DD"}),
    )

    is_active = django_filters.BooleanFilter(
        field_name="is_active",
        label="Blog Active",
    )

    class Meta:
        model = Blog
        fields = ["author_id", "publish_date", "is_active"]


class BlogReviewFilter(django_filters.FilterSet):
    user_id = django_filters.CharFilter(
        field_name="user__id", lookup_expr="exact",
        label="User ID",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by user id"}
        )
    )

    blog_id = django_filters.CharFilter(
        field_name="blog__id", lookup_expr="exact",
        label="Blog ID",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by blog id"}
        )
    )

    class Meta:
        model = BlogReview
        fields = ["user_id", "blog_id"]
