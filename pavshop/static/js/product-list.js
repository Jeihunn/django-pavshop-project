window.addEventListener("load", function () {
  fetchCategories();
  fetchTags();
  fetchBrands();
  fetchColors();
  fetchProductVersions();
});

function fetchCategories() {
  fetch(
    "/api/product-categories/?page_size=20&is_active=true&order_by=name"
  )
    .then((response) => {
      if (!response.ok) {
        throw new Error("API request failed.");
      }
      return response.json();
    })
    .then((data) => {
      let categories = data.results;
      let categoryList = document.getElementById("category-list");
      let html = "";

      for (let i = 0; i < categories.length; i++) {
        html += `<li><a href="#."> ${categories[i].name} <span>${categories[i].product_count}</span></a></li>`;
      }

      categoryList.innerHTML = html;
    })
    .catch((error) => {
      console.error("An error occurred during the API request:", error.message);
    });
}

function fetchTags() {
  fetch(
    "/api/product-tags/?page_size=10&is_active=true&order_by=-created_at"
  )
    .then((response) => {
      if (!response.ok) {
        throw new Error("API request failed.");
      }
      return response.json();
    })
    .then((data) => {
      let tags = data.results;
      let tagList = document.getElementById("tag-list");
      let html = "";

      for (let i = 0; i < tags.length; i++) {
        html += `<li><a href="#.">${tags[i].name}</a></li>`;
      }

      tagList.innerHTML = html;
    })
    .catch((error) => {
      console.error("An error occurred during the API request:", error.message);
    });
}

function fetchBrands() {
  fetch("/api/product-brands/?page_size=10&is_active=true")
    .then((response) => {
      if (!response.ok) {
        throw new Error("API request failed.");
      }
      return response.json();
    })
    .then((data) => {
      let brands = data.results;
      let brandList = document.getElementById("brand-list");
      let html = "";

      for (let i = 0; i < brands.length; i++) {
          html += `<li><a href="#.">${brands[i].name}</a></li>`;
      }

      brandList.innerHTML = html;
    })
    .catch((error) => {
      console.error("An error occurred during the API request:", error.message);
    });
}

function fetchColors() {
  fetch("/api/product-colors/?page_size=30&is_active=true")
    .then((response) => {
      if (!response.ok) {
        throw new Error("API request failed.");
      }
      return response.json();
    })
    .then((data) => {
      let colors = data.results;
      let colorList = document.getElementById("color-list");
      let html = "";

      for (let i = 0; i < colors.length; i++) {
          html += `<li><a href="#." style="background:${colors[i].hex_code};"></a></li>`;
      }

      colorList.innerHTML = html;
    })
    .catch((error) => {
      console.error("An error occurred during the API request:", error.message);
    });
}

function fetchProductVersions() {
  fetch("/api/product-versions/?page_size=9&is_active=true&order_by=-created_at")
    .then((response) => {
      if (!response.ok) {
        throw new Error("API request failed.");
      }
      return response.json();
    })
    .then((data) => {
      let versions = data.results;
      let versionList = document.getElementById("product-list");
      let html = "";

      for (let i = 0; i < versions.length; i++) {
        let discount = 0;
        for (d of versions[i].discounts) {
          if (d.is_active) {
            discount += d.percent;
          }
        }

        let discountHtml = "";
        let oldPriceHtml = "";
        if (discount > 0) {
          discountHtml = `<div class="on-sale">${discount}% <span>OFF</span></div>`;
          oldPriceHtml = `<span class="price old-price"><small>$</small>${versions[i].price}</span>`;
        }

        html += `
        <!-- Item -->
        <div class="col-md-4">
          <div class="item height-400"> 
            <!-- Sale Tags -->
            ${discountHtml}
            
            <!-- Item img -->
            <div class="item-img"> 
              <img class="img-1 image-container" src="${versions[i].cover_image}" alt="" >
              <!-- Overlay -->
              <div class="overlay">
                <div class="position-center-center">
                  <div class="inn">
                    <a href="${versions[i].cover_image}" data-lighter><i class="icon-magnifier"></i></a> 
                    <a href="#."><i class="icon-basket"></i></a> 
                    <a href="#."><i class="icon-heart"></i></a>
                  </div>
                </div>
              </div>
            </div>
            <!-- Item Name -->
            <div class="item-name text-nowrap"> <a href="#.">${versions[i].title}</a></div>

            <!-- Price --> 
            <div class="flex-container">
              <span class="price"><small>$</small>${versions[i].price * (100 - discount) / 100}</span>
              ${oldPriceHtml}
            </div>

          </div>
        </div>
      `;
      }

      versionList.innerHTML = html;
    })
    .catch((error) => {
      console.error("An error occurred during the API request:", error.message);
    });
}
