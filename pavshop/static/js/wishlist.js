function toggleWishlist2x(button) {
  const productVersionId = button.getAttribute("data-product-version-id");

  const url = `${location.origin}/toggle-wishlist/?product_version_id=${productVersionId}`
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      if (data.is_added) {
        button.innerHTML = '<i class="fa fa-2x fa-heart text-danger"></i>';
      } else {
        button.innerHTML = '<i class="fa fa-2x fa-heart-o"></i>';
      }
    });
}

function toggleWishlist(button) {
  const productVersionId = button.getAttribute("data-product-version-id");

  const url = `${location.origin}/toggle-wishlist/?product_version_id=${productVersionId}`
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      if (data.is_added) {
        button.innerHTML = '<i class="fa fa-heart text-danger"></i>';
      } else {
        button.innerHTML = '<i class="fa fa-heart-o"></i>';
      }
    });
}

function removeWishlist(button) {
  const productVersionId = button.getAttribute("data-product-version-id");
  const cardDetail = document.querySelector(`#cart-detail-${productVersionId}`);
  const wishlistCount = document.querySelector(".wishlist-count");
  const wishlistContainer = document.querySelector(".wishlist-container");

  const url = `${location.origin}/remove-wishlist/?product_version_id=${productVersionId}`
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        cardDetail.remove();
        wishlistCount.innerHTML = data.wishlist_count;
      }

      if (!data.wishlist_count) {
        wishlistContainer.innerHTML = `
        <div class="alert alert-info">
          <p><strong>Oops!</strong> There are currently no items in your wishlist.</p>
          <p>Please feel free to browse our <a href="/products/">products page</a> for exciting items to add.</p>
        </div>
    `;
      }
    });
}
