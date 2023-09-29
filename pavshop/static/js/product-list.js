window.addEventListener("load", function () {
  const sortBy = document.querySelector(".sort-by select").value;
  localStorage.setItem("order_by", sortBy);

  fetchCategories();
  fetchTags();
  fetchBrands();
  fetchColors();
  fetchProductVersions();
});

function fetchCategories() {
  const url = `${location.origin}/api/product-categories/?page_size=20&is_active=true&order_by=name`;
  fetch(url)
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
        html += `<li><a class="category-buttons" data-category-id="${categories[i].id}" style="cursor: pointer" onclick="filterCategory(this)"> ${categories[i].name} <span>${categories[i].product_count}</span></a></li>`;
      }

      categoryList.innerHTML = html;
    })
    .catch((error) => {
      console.error("An error occurred during the API request:", error.message);
    });
}

function fetchTags() {
  const url = `${location.origin}/api/product-tags/?page_size=10&is_active=true&order_by=-created_at`;
  fetch(url)
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
        html += `<li><a class="tag-buttons" data-tag-id="${tags[i].id}" style="cursor: pointer" onclick="filterTag(this)">${tags[i].name}</a></li>`;
      }

      tagList.innerHTML = html;
    })
    .catch((error) => {
      console.error("An error occurred during the API request:", error.message);
    });
}

function fetchBrands() {
  const url = `${location.origin}/api/product-brands/?page_size=10&is_active=true`;
  fetch(url)
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
        html += `<li><a class="brand-buttons" data-brand-id="${brands[i].id}" style="cursor: pointer" onclick="filterBrand(this)">${brands[i].name}</a></li>`;
      }

      brandList.innerHTML = html;
    })
    .catch((error) => {
      console.error("An error occurred during the API request:", error.message);
    });
}

function fetchColors() {
  const url = `${location.origin}/api/product-colors/?page_size=30&is_active=true`;
  fetch(url)
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
        html += `<li><a class="color-buttons" data-color-id="${colors[i].id}" style="cursor: pointer; background:${colors[i].hex_code};" onclick="filterColor(this)"></a></li>`;
      }

      colorList.innerHTML = html;
    })
    .catch((error) => {
      console.error("An error occurred during the API request:", error.message);
    });
}

function fetchProductVersions() {
  let url = `${location.origin}/api/product-versions/?page_size=9&is_active=true`;
  const orderBy = localStorage.getItem("order_by");
  const urlExtra = url + `&order_by=${orderBy}`;

  fetch(urlExtra)
    .then((response) => {
      if (!response.ok) {
        throw new Error("API request failed.");
      }
      return response.json();
    })
    .then((data) => {
      localStorage.setItem("data-url", url);

      getPagination(data);

      getVersions(data);
    })
    .catch((error) => {
      console.error("An error occurred during the API request:", error.message);
    });
}

// Filters
function filterCategory(button) {
  const categoryId = button.getAttribute("data-category-id");
  const url = `${location.origin}/api/product-versions/?page_size=9&is_active=true&category__id=${categoryId}`;
  const orderBy = localStorage.getItem("order_by");
  const urlExtra = url + `&order_by=${orderBy}`;

  fetch(urlExtra)
    .then((response) => {
      if (!response.ok) {
        throw new Error("API request failed.");
      }
      return response.json();
    })
    .then((data) => {
      localStorage.setItem("data-url", url);

      cleanSearchInput();

      cleanActive();
      button.classList.add("a-active");

      getPagination(data);

      getVersions(data);
    })
    .catch((error) => {
      console.error("An error occurred during the API request:", error.message);
    });
}

function filterTag(button) {
  const tagId = button.getAttribute("data-tag-id");
  const url = `${location.origin}/api/product-versions/?page_size=9&is_active=true&tag__id=${tagId}`;
  const orderBy = localStorage.getItem("order_by");
  const urlExtra = url + `&order_by=${orderBy}`;

  fetch(urlExtra)
    .then((response) => {
      if (!response.ok) {
        throw new Error("API request failed.");
      }
      return response.json();
    })
    .then((data) => {
      localStorage.setItem("data-url", url);

      cleanSearchInput();

      cleanActive();
      button.classList.add("a-active");

      getPagination(data);

      getVersions(data);
    })
    .catch((error) => {
      console.error("An error occurred during the API request:", error.message);
    });
}

function filterBrand(button) {
  const brandId = button.getAttribute("data-brand-id");
  const url = `${location.origin}/api/product-versions/?page_size=9&is_active=true&brand__id=${brandId}`;
  const orderBy = localStorage.getItem("order_by");
  const urlExtra = url + `&order_by=${orderBy}`;

  fetch(urlExtra)
    .then((response) => {
      if (!response.ok) {
        throw new Error("API request failed.");
      }
      return response.json();
    })
    .then((data) => {
      localStorage.setItem("data-url", url);

      cleanSearchInput();

      cleanActive();
      button.classList.add("a-active");

      getPagination(data);

      getVersions(data);
    })
    .catch((error) => {
      console.error("An error occurred during the API request:", error.message);
    });
}

function filterColor(button) {
  const colorId = button.getAttribute("data-color-id");
  const url = `${location.origin}/api/product-versions/?page_size=9&is_active=true&color__id=${colorId}`;
  const orderBy = localStorage.getItem("order_by");
  const urlExtra = url + `&order_by=${orderBy}`;

  fetch(urlExtra)
    .then((response) => {
      if (!response.ok) {
        throw new Error("API request failed.");
      }
      return response.json();
    })
    .then((data) => {
      localStorage.setItem("data-url", url);

      cleanSearchInput();

      cleanActive();

      getPagination(data);

      getVersions(data);
    })
    .catch((error) => {
      console.error("An error occurred during the API request:", error.message);
    });
}

// search product
const searchFOrm = document.querySelector(".product-search");
const searchInput = searchFOrm.querySelector("input");
searchFOrm.addEventListener("submit", (event) => {
  event.preventDefault();

  let url = `${location.origin}/api/product-versions/?page_size=9&is_active=true&search=${searchInput.value}`;
  const orderBy = localStorage.getItem("order_by");
  const urlExtra = url + `&order_by=${orderBy}`;
  fetch(urlExtra)
    .then((response) => {
      if (!response.ok) {
        throw new Error("API request failed.");
      }
      return response.json();
    })
    .then((data) => {
      localStorage.setItem("data-url", url);

      cleanActive();

      getPagination(data);

      getVersions(data);
    })
    .catch((error) => {
      console.error("An error occurred during the API request:", error.message);
    });
});

// Pagination Click
function paginationClick(button) {
  let url = localStorage.getItem("data-url");
  const order_by = localStorage.getItem("order_by");
  let pageNumber = button.getAttribute("data-page-number");
  const urlExtra = url + `&order_by=${order_by}&page=${pageNumber}`;
  fetch(urlExtra)
    .then((response) => {
      if (!response.ok) {
        throw new Error("API request failed.");
      }
      return response.json();
    })
    .then((data) => {
      getPagination(data);

      getVersions(data);
    })
    .catch((error) => {
      console.error("An error occurred during the API request:", error.message);
    });
}

// sort change
function sortChange(button) {
  const selectValue = button.value;
  localStorage.setItem("order_by", selectValue);

  let url = localStorage.getItem("data-url");
  const order_by = localStorage.getItem("order_by");
  const urlExtra = url + `&order_by=${order_by}`;

  fetch(urlExtra)
    .then((response) => {
      if (!response.ok) {
        throw new Error("API request failed.");
      }
      return response.json();
    })
    .then((data) => {
      getPagination(data);

      getVersions(data);
    })
    .catch((error) => {
      console.error("An error occurred during the API request:", error.message);
    });
}

// Wishlist
function toggleWishlist(button) {
  const productVersionId = button.getAttribute("data-product-version-id");
  const url = `/toggle-wishlist/?product_version_id=${productVersionId}`;
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      if (data.is_added) {
        button.innerHTML = '<i class="fa fa-heart text-danger"></i>';
      } else {
        button.innerHTML = '<i class="fa fa-heart-o"></i>';
      }
    })
    .catch((error) => {
      console.error("An error occurred during the API request:", error.message);
    });
}

// get vetsions
function getVersions(data) {
  let versions = data.results;
  let versionList = document.getElementById("product-list");
  let html = "";

  if (versions.length > 0) {
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
      if (isAuthenticated) {
        var heartIcon = `<a data-product-version-id="${versions[i].id}" onclick="toggleWishlist(this)" style="cursor: pointer;">
                          <i class="fa fa-heart-o"></i>
                        </a>`;
        var basketIcon = `<a data-product-version-id="${versions[i].id}" onclick="addToCart(this)" style="cursor: pointer;">
                            <i class="icon-basket"></i>
                          </a>`;
      } else {
        var heartIcon = `<a href="/login/">
                          <i class="fa fa-heart-o"></i>
                        </a>`;
        var basketIcon = `<a href="/login/">
                            <i class="icon-basket"></i>
                          </a>`;
      }

      html += `
      <!-- Item -->
      <div class="col-md-4">
        <div class="item height-400"> 
          <!-- Sale Tags -->
          ${discountHtml}
          
          <!-- Item img -->
          <div class="item-img"> 
            <img class="img-1 image-container" src="${
              versions[i].cover_image
            }" alt="" >
            <!-- Overlay -->
            <div class="overlay">
              <div class="position-center-center">
                <div class="inn">
                  <a href="${
                    versions[i].cover_image
                  }" data-lighter><i class="icon-magnifier"></i></a> 
                  ${basketIcon}
                  ${heartIcon}
                </div>
              </div>
            </div>
          </div>
          <!-- Item Name -->
          <div class="item-name text-nowrap"> <a href="/product/${
            versions[i].slug
          }/">${versions[i].title}</a></div>
  
          <!-- Price --> 
          <div class="flex-container">
            <span class="price"><small>$</small>${
              (versions[i].price * (100 - discount)) / 100
            }</span>
            ${oldPriceHtml}
          </div>
  
        </div>
      </div>
    `;

      const sortBy = document.querySelector(".sort-by");
      sortBy.style.display = "block";
    }
  } else {
    html = `<div class="alert alert-info">
              <p><strong>Sorry, no products found at the moment.</strong></p>
            </div>
            `;

    const sortBy = document.querySelector(".sort-by");
    sortBy.style.display = "none";
  }

  versionList.innerHTML = html;
}

// get pagination
function getPagination(data) {
  const pagination = document.querySelector("#pagination");

  const productNum = document.querySelector(".product-num");
  const previousPage = data.previous;
  const nextPage = data.next;
  const pageCount = data.page_count;
  const currentPage = data.current_page;
  const pageSize = data.page_size;
  const totalCount = data.count;
  const startIndex = (currentPage - 1) * pageSize + 1;
  const endIndex = Math.min(currentPage * pageSize, totalCount);

  if (totalCount === 0) {
    productNum.innerHTML = `0 products`;
  } else {
    productNum.innerHTML = `Showing ${startIndex} - ${endIndex} of ${totalCount} products`;
  }

  // Pagination
  pagination.innerHTML = "";
  if (totalCount > pageSize) {
    let previousPageHTML = "";
    let firstPageHTML = "";
    if (previousPage) {
      previousPageHTML = `<li><a data-page-number="${
        currentPage - 1
      }" style="cursor: pointer" onclick="paginationClick(this)">${
        currentPage - 1
      }</a></li>`;
      firstPageHTML = `<li><a data-page-number="1" style="cursor: pointer" onclick="paginationClick(this)"><i class="fa fa-angle-double-left"></i></a></li>`;
    }

    let nextPageHTML = "";
    let lastPageHTML = "";
    if (nextPage) {
      nextPageHTML = `<li><a data-page-number="${
        currentPage + 1
      }" style="cursor: pointer" onclick="paginationClick(this)">${
        currentPage + 1
      }</a></li>`;
      lastPageHTML = `<li><a data-page-number="${pageCount}" style="cursor: pointer" onclick="paginationClick(this)"><i class="fa fa-angle-double-right"></i></a></li>`;
    }

    let currentPageHTML = "";
    currentPageHTML = `<li class="active"><a data-page-number="${currentPage}" style="cursor: pointer" onclick="paginationClick(this)">${currentPage}</a></li>`;

    pagination.innerHTML =
      firstPageHTML +
      previousPageHTML +
      currentPageHTML +
      nextPageHTML +
      lastPageHTML;
  }
}

// clean a-active
function cleanActive() {
  const categoryButtons = document.querySelectorAll(".category-buttons");
  const tagButtons = document.querySelectorAll(".tag-buttons");
  const brandButtons = document.querySelectorAll(".brand-buttons");

  for (let i = 0; i < categoryButtons.length; i++) {
    categoryButtons[i].classList.remove("a-active");
  }

  for (let i = 0; i < tagButtons.length; i++) {
    tagButtons[i].classList.remove("a-active");
  }

  for (let i = 0; i < brandButtons.length; i++) {
    brandButtons[i].classList.remove("a-active");
  }
}

// clean search input
function cleanSearchInput() {
  const searchInput = document.querySelector(".product-search input");
  searchInput.value = "";
}
