function removeCartItem(button) {
  const cartItemId = button.getAttribute("data-cart-item-id");
  const itemDetail = document.querySelector(`#cart-item-${cartItemId}`);
  const shoppingCartContainer = document.querySelector(
    ".shopping-cart-container"
  );
  const pItemDetail = document.querySelector(`#p-cart-item-${cartItemId}`);
  const totalCost = document.querySelector(`#total-cost`);
  const headerItemDetail = document.querySelector(
    `#header-cart-item-${cartItemId}`
  );
  const subtotal = document.querySelector("#subtotal");
  const checkoutButton = document.querySelector(".checkout-button");
  const liHeaderBasketCount = document.querySelector("#header-basket-count");
  const headerBasketCount = document.querySelector("#header-basket-count span");

  fetch(`/remove-from-cart/?cart_item_id=${cartItemId}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        itemDetail.remove();
        pItemDetail.remove();
        totalCost.innerHTML = data.cart_total_price;
        headerItemDetail.remove();
        subtotal.innerHTML = data.cart_total_price;
        headerBasketCount.innerHTML = data.basket_count;
      }

      if (!data.basket_count) {
        shoppingCartContainer.innerHTML = `
            <div class="alert alert-info">
                There are no items in your cart.
                <span class="alert-link">
                <a href="/products/">Click here to view products.</a>
                </span>
            </div>
      `;
        checkoutButton.remove();
        headerBasketCount.remove();
      }
    });
}

function addToCartQuantity(button) {
  const product_version_id = button.getAttribute("data-product-version-id");
  const quantity = document.querySelector(".qty-select").value;
  const liHeaderBasketCount = document.querySelector("#header-basket-count");

  fetch(
    `/add-to-cart/?product_version_id=${product_version_id}&quantity=${quantity}`
  )
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        showToastify("Item added to cart.", "success", 1000);
        liHeaderBasketCount.innerHTML = `
          <span class="badge">${data.basket_count}</span>
        `;
      } else if (!data.success) {
        showToastify("Item not added to cart.", "warning", 1000);
      }
    });
}

function addToCart(button) {
  const product_version_id = button.getAttribute("data-product-version-id");
  const liHeaderBasketCount = document.querySelector("#header-basket-count");

  fetch(`/add-to-cart/?product_version_id=${product_version_id}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        showToastify("Item added to cart.", "success", 1000);
        liHeaderBasketCount.innerHTML = `
          <span class="badge">${data.basket_count}</span>
        `;
      } else if (!data.success) {
        showToastify("Item not added to cart.", "warning", 1000);
      }
    });
}

function showCart() {
  const liHeaderBasket = document.querySelector(".user-basket");
  const userId = liHeaderBasket.getAttribute("data-user-id");

  fetch(`/api/shopping-cart/?user__id=${userId}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("API request failed.");
      }
      return response.json();
    })
    .then((data) => {
      console.log(data);

      let cart_itemsHTML = "";
      for (let item of data.results[0].items) {
        if (item.product_version.is_active) {
          cart_itemsHTML += `
          <li id="header-cart-item-${item.id}">
            <div class="media-left">
              <div class="cart-img"> <a href="#"> <img class="media-object img-responsive" src="${item.product_version.cover_image}" alt=""> </a> </div>
            </div>
            <div class="media-body">
              <h6 class="media-heading">${item.product_version.title}</h6>
              <span class="price">${item.product_version.discounted_price} USD</span> <span class="qty">QTY": ${item.quantity}</span> 
            </div>
          </li>
        `;
        }
      }

      let subtotalHTML = "";
      if (data.results[0].total_price > 0) {
        subtotalHTML = `
          <h5 class="text-center">
            SUBTOTAL: 
            <span id="subtotal">${data.results[0].total_price}</span>
          </h5>
        `;
      } else {
        subtotalHTML = `
          <div class="alert alert-info">
            YOUR BASKET IS EMPTY
          </div>
        `;
      }

      let checkoutHTML = "";
      if (data.results[0].total_price > 0) {
        checkoutHTML = `
          <div class="col-xs-6 checkout-button"> <a href="/checkout/" class="btn">CHECK OUT</a></div>
        `;
      }

      liHeaderBasket.innerHTML = `
      <a href="#" id="dropdown-basket" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="true" onclick="showCart()">
        <i class="icon-basket-loaded"></i>
      </a>
  
      <ul class="dropdown-menu">
        ${cart_itemsHTML}
        ${subtotalHTML}
          
        <li class="margin-0">
          <div class="row">
            <div class="col-xs-6"> <a href="/shopping-cart/" class="btn">VIEW CART</a></div>
            ${checkoutHTML}
          </div>
        </li>

      </ul>
    `;
    })
    .catch((error) => {
      console.error("An error occurred during the API request:", error.message);
    });
}

function showToastify(message, type, duration) {
  if (type.toLowerCase() === "success") {
    var background = "#4CAF50";
    var color = "#fff";
  } else if (type.toLowerCase() === "warning") {
    var background = "#ff9800";
    var color = "#fff";
  } else if (type.toLowerCase() === "error") {
    var background = "#f44336";
    var color = "#fff";
  } else {
    var background = "#4CAF50";
    var color = "#fff";
  }

  Toastify({
    text: message,
    duration: duration || 400,
    close: false,
    gravity: "top",
    position: "right",
    style: {
      background: background,
      color: color,
      borderRadius: "5px",
      padding: "10px 20px",
      fontSize: "16px",
      opacity: 0.9,
    },
  }).showToast();
}
