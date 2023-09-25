from product.models import ShoppingCart


def shopping_cart_context(request):
    if request.user.is_authenticated:
        shopping_cart, created = ShoppingCart.objects.get_or_create(user=request.user)
        cart_items = shopping_cart.items.filter(product_version__is_active=True)
        basket_count = 0
        for item in cart_items:
            basket_count += item.quantity
        return {
            "shopping_cart": shopping_cart,
            "cart_items": cart_items,
            "basket_count": basket_count,
        }
    return {}
