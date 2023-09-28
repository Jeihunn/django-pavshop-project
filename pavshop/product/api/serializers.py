from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from product.models import (
    Product,
    ProductVersion,
    ProductVersionImage,
    Discount,
    ProductCategory,
    ProductTag,
    Color,
    Designer,
    Brand,
    Wishlist,
    CartItem,
    ShoppingCart
)
from blog.api.serializers import UserSerializer


class ProductCategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api_product:api_product_category_detail_view",
        lookup_field="pk"
    )

    name_en = serializers.CharField(required=True)
    name_az = serializers.CharField(required=True)

    class Meta:
        model = ProductCategory
        fields = (
            "url",
            "id",
            "name",
            "name_en",
            "name_az",
            "product_count",
            "slug",
            "is_active",
            "created_at",
            "updated_at"
        )
        read_only_fields = (
            "is_active",
        )

    def validate_name_en(self, name_en):
        if self.instance:
            if ProductCategory.objects.filter(name_en=name_en).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError(
                    _("A product category with the same name (name_en) already exists."))
        else:
            if ProductCategory.objects.filter(name_en=name_en).exists():
                raise serializers.ValidationError(
                    _("A product category with the same name (name_en) already exists."))
        return name_en

    def validate_name_az(self, name_az):
        if self.instance:
            if ProductCategory.objects.filter(name_az=name_az).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError(
                    _("A product category with the same name (name_az) already exists."))
        else:
            if ProductCategory.objects.filter(name_az=name_az).exists():
                raise serializers.ValidationError(
                    _("A product category with the same name (name_az) already exists."))
        return name_az


class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = (
            "id",
            "name",
            "product_count",
            "slug",
            "is_active",
            "created_at",
            "updated_at"
        )


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = (
            "id",
            "name",
            "hex_code",
            "is_active",
            "created_at",
            "updated_at"
        )


class DesignerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designer
        fields = (
            "id",
            "name",
            "is_active",
            "created_at",
            "updated_at"
        )


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            "id",
            "name",
            "is_active",
            "slug",
            "created_at",
            "updated_at"
        )


class ProductListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api_product:api_product_detail_view",
        lookup_field="pk"
    )

    brand = BrandSerializer()
    product_categories = ProductCategorySerializer(many=True)
    product_tags = ProductTagSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "url",
            "id",
            "title",
            "title_en",
            "title_az",
            "brand",
            "product_categories",
            "product_tags",
            "slug",
        )


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    title_en = serializers.CharField(required=True)
    title_az = serializers.CharField(required=True)
    brand = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(),
        required=True
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "title_en",
            "title_az",
            "brand",
            "product_categories",
            "product_tags",
            "slug",
        )


class ProductVersionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVersionImage
        fields = (
            "id",
            "image",
            "is_active",
        )


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = (
            "id",
            "name",
            "percent",
            "is_active",
        )


class ProductVersionListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api_product:api_product_version_detail_view",
        lookup_field="pk"
    )

    product = ProductListSerializer()
    designer = DesignerSerializer()
    colors = ColorSerializer(many=True)
    images = ProductVersionImageSerializer(many=True)
    discounts = DiscountSerializer(many=True)

    class Meta:
        model = ProductVersion
        fields = (
            "url",
            "id",
            "title",
            "title_en",
            "title_az",
            "product",
            "designer",
            "colors",
            "price",
            "quantity",
            "description_en",
            "description_az",
            "cover_image",
            "images",
            "discounts",
            "slug",
            "is_active",
        )


class ProductVersionCreateUpdateSerializer(serializers.ModelSerializer):
    title_en = serializers.CharField(required=True)
    title_az = serializers.CharField(required=True)

    class Meta:
        model = ProductVersion
        fields = (
            "id",
            "product",
            "designer",
            "colors",
            "title_en",
            "title_az",
            "price",
            "quantity",
            "description_en",
            "description_az",
            "cover_image",
            "slug",
            "is_active",
        )

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError(
                _("Price cannot be negative."))
        return value

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError(
                _("Quantity cannot be negative."))
        return value


class WishlistListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api_product:api_wishlist_detail_view",
        lookup_field="pk"
    )

    user = UserSerializer()

    class Meta:
        model = Wishlist
        fields = (
            "url",
            "id",
            "user",
            "product_versions",
        )


class WishlistCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = (
            "id",
            "user",
            "product_versions",
        )
        read_only_fields = (
            "user",
        )

    def create(self, validated_data):
        if self.context["request"].user.is_authenticated:
            user = self.context["request"].user
            if Wishlist.objects.filter(user=user).exists():
                raise serializers.ValidationError(
                    _("You already have a wishlist."))
            validated_data["user"] = user
        return super().create(validated_data)


class ProductVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVersion
        fields = (
            "id",
            "title",
            "price",
            "discounted_price",
            "quantity",
            "cover_image",
            "is_active",
        )


class CartItemSerializer(serializers.ModelSerializer):
    product_version = ProductVersionSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = (
            "id",
            "cart",
            "product_version",
            "quantity",
            "total_price",
        )


class ShoppingCartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = (
            "id",
            "user",
            "items",
            "total_price",
        )
