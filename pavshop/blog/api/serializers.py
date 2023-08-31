from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from blog.models import Blog, BlogReview, BlogCategory, BlogTag
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model

User = get_user_model()


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = (
            "id",
            "name",
            "slug",
            "is_active",
        )


class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = (
            "id",
            "name",
            "slug",
            "is_active",
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
        )


class BlogListSerializer(serializers.ModelSerializer):
    content_preview = serializers.SerializerMethodField()

    author = UserSerializer()
    blog_categories = BlogCategorySerializer(many=True)
    blog_tags = BlogTagSerializer(many=True)

    class Meta:
        model = Blog
        fields = (
            "id",
            "title",
            "author",
            "blog_categories",
            "blog_tags",
            "cover_image",
            "publish_date",
            "slug",
            "is_active",
            "content_preview",
        )

    def get_content_preview(self, obj):
        preview_length = 100
        content = strip_tags(obj.content)[:preview_length]
        if len(strip_tags(obj.content)) > preview_length:
            content += "..."
        return content


class BlogReviewListSerializer(serializers.ModelSerializer):
    sub_reviews = serializers.SerializerMethodField()

    url = serializers.HyperlinkedIdentityField(
        view_name="api_blog:api_blog_review_detail_view",
        lookup_field="pk"
    )

    class Meta:
        model = BlogReview
        fields = (
            "url",
            "id",
            "blog",
            "parent",
            "user",
            "full_name",
            "email",
            "subject",
            "comment",
            "created_at",
            "updated_at",
            "sub_reviews"
        )

    def get_sub_reviews(self, obj):
        if obj.children:
            children_data = BlogReviewListSerializer(
                obj.children, many=True, context=self.context).data
            return children_data


class BlogReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogReview
        fields = (
            "blog",
            "parent",
            "user",
            "full_name",
            "email",
            "subject",
            "comment",
        )

        read_only_fields = ("user",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.context["request"].user.is_authenticated:
            self.fields["full_name"].read_only = True
            self.fields["email"].read_only = True
        else:
            self.fields["full_name"].required = True
            self.fields["email"].required = True

    def check_max_parent_nesting(self, parent, max_parent_nesting=1):  # custom method
        nesting_level = 1
        current_parent = parent

        while current_parent.parent and nesting_level <= max_parent_nesting:
            current_parent = current_parent.parent
            nesting_level += 1

        return nesting_level > max_parent_nesting

    def validate_parent(self, value):
        blog_id = self.initial_data.get("blog")  # str

        max_parent_nesting = 1

        if value:
            if str(value.blog.id) != blog_id:
                raise serializers.ValidationError(
                    _("The selected parent review does not belong to the chosen blog."))
            elif self.check_max_parent_nesting(value, max_parent_nesting):
                raise serializers.ValidationError(
                    _("The selected parent comment exceeds the designated maximum sub-comment level. Maximum level: {}").format(max_parent_nesting))

        return value

    def validate_full_name(self, value):
        if not value:
            raise serializers.ValidationError(_("This field is required."))
        return value

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError(_("This field is required."))
        return value

    def create(self, validated_data):
        if self.context["request"].user.is_authenticated:
            validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class BlogReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogReview
        fields = (
            "id",
            "blog",
            "parent",
            "user",
            "full_name",
            "email",
            "subject",
            "comment",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("user", "full_name", "email", "parent", "blog")
