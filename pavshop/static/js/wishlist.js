function toggleWishlist(button) {
  const productVersionId = button.getAttribute("data-product-version-id");
  fetch(`/toggle-wishlist/?product_version_id=${productVersionId}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.is_added) {
        button.innerHTML = '<i class="fa fa-2x fa-heart text-danger"></i>';
      } else {
        button.innerHTML = '<i class="fa fa-2x fa-heart-o"></i>';
      }
    });
}

function removeWishlist(button) {
  const productVersionId = button.getAttribute("data-product-version-id");
  const cardDetail = document.querySelector(`#cart-detail-${productVersionId}`);
  fetch(`/remove-wishlist/?product_version_id=${productVersionId}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        cardDetail.remove();
      }
    });
}
