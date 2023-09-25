from django.urls import path
from . import views as api_views

app_name = "api_product"
urlpatterns = [
    path("product-tags/", api_views.ProducTagListAPIView.as_view(),
         name="api_product_tag_list_view"),
    path("product-colors/", api_views.ColorListAPIView.as_view(),
         name="api_color_list_view"),
    path("product-designers/", api_views.DesignerListAPIView.as_view(),
         name="api_designer_list_view"),
    path("product-brands/", api_views.BrandListAPIView.as_view(),
         name="api_brand_list_view"),

    path("product-categories/", api_views.ProductCategoryListCreateAPIView.as_view(),
         name="api_product_category_list_create_view"),
    path("product-category/<int:pk>/", api_views.ProductCategoryDetailAPIView.as_view(),
         name="api_product_category_detail_view"),

    path("products/", api_views.ProductListCreateAPIView.as_view(),
         name="api_product_list_create_view"),
    path("product/<int:pk>/", api_views.ProductDetailAPIView.as_view(),
         name="api_product_detail_view"),

    path("product-versions/", api_views.ProductVersionListCreateAPIView.as_view(),
         name="api_product_version_list_create_view"),
    path("product-version/<int:pk>/", api_views.ProductVersionDetailAPIView.as_view(),
         name="api_product_version_detail_view"),

    path("wishlists/", api_views.WishlistListCreateAPIView.as_view(),
         name="api_wishlist_list_create_view"),
    path("wishlist/<int:pk>/", api_views.WishlistDetailAPIView.as_view(),
         name="api_wishlist_detail_view"),

    path("shopping-cart/", api_views.ShoppingCartListAPIView.as_view(),
         name="api_shopping_cart_list_view"),
]
