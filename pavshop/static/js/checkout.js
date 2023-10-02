const placeOrder = document.getElementById("place-order");
const sameAddressCheckbox = document.getElementById("checkbox-same-address");
const readAndAcceptCheckbox = document.getElementById("read-and-accept");

placeOrder.addEventListener("click", function () {
  if (readAndAcceptCheckbox.checked) {
    billingFormSubmit();

    if (!sameAddressCheckbox.checked) {
      shippingFormSubmit();
    }
  } else {
    alert("Please accept the terms and conditions");
  }
});

// billing
function billingFormSubmit() {
  const billingForm = document.getElementById("billing-form");
  const errorList = billingForm.querySelector(".errorlist");
  const shippingForm = document.getElementById("shipping-form");
  const shippingErrorList = shippingForm.querySelector(".errorlist");

  const formData = {
    first_name: billingForm.first_name.value,
    last_name: billingForm.last_name.value,
    company_name: billingForm.company_name.value,
    address: billingForm.address.value,
    city: billingForm.city.value,
    country: billingForm.country.value,
    email: billingForm.email.value,
    phone_number: billingForm.phone_number.value,
  };

  const url = `${location.origin}/api/billing-address/`;
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": billingForm.csrfmiddlewaretoken.value,
    },
    body: JSON.stringify(formData),
  })
    .then((response) => {
      if (response.ok) {
        billingForm.reset();
        errorList.innerHTML = "";

        if (sameAddressCheckbox.checked) {
          shippingFormChecked(formData);
          shippingErrorList.innerHTML = "";
        }
      } else {
        response.json().then((data) => {
          console.error("Error code:", response.status);
          console.error("Error message:", data);

          html = "";
          for (let [key, value] of Object.entries(data)) {
            html += `<li class="error">${key
              .replace(/_/g, " ")
              .toUpperCase()}: ${value}</li>`;
          }
          errorList.innerHTML = html;

          if (sameAddressCheckbox.checked) {
            // shippingForm.reset();
            shippingErrorList.innerHTML = "";
          }
        });
      }
    })
    .catch((error) => {
      console.error("Catch Error:", error);
    });
}

// shipping
function shippingFormSubmit() {
  const shippingForm = document.getElementById("shipping-form");
  const errorList = shippingForm.querySelector(".errorlist");

  const formData = {
    first_name: shippingForm.first_name.value,
    last_name: shippingForm.last_name.value,
    company_name: shippingForm.company_name.value,
    address: shippingForm.address.value,
    city: shippingForm.city.value,
    country: shippingForm.country.value,
    email: shippingForm.email.value,
    phone_number: shippingForm.phone_number.value,
  };

  const url = `${location.origin}/api/shipping-address/`;
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": shippingForm.csrfmiddlewaretoken.value,
    },
    body: JSON.stringify(formData),
  })
    .then((response) => {
      if (response.ok) {
        shippingForm.reset();
        errorList.innerHTML = "";
      } else {
        response.json().then((data) => {
          console.error("Error code:", response.status);
          console.error("Error message:", data);

          html = "";
          for (let [key, value] of Object.entries(data)) {
            html += `<li class="error">${key
              .replace(/_/g, " ")
              .toUpperCase()}: ${value}</li>`;
          }
          errorList.innerHTML = html;
        });
      }
    })
    .catch((error) => {
      console.error("Catch Error:", error);
    });
}

// shipping checked
function shippingFormChecked(form_data) {
  const shippingForm = document.getElementById("shipping-form");
  const errorList = shippingForm.querySelector(".errorlist");

  const formData = form_data;

  const url = `${location.origin}/api/shipping-address/`;
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": shippingForm.csrfmiddlewaretoken.value,
    },
    body: JSON.stringify(formData),
  })
    .then((response) => {
      if (response.ok) {
        shippingForm.reset();
        errorList.innerHTML = "";
      } else {
        response.json().then((data) => {
          console.error("Error code:", response.status);
          console.error("Error message:", data);

          errorList.innerHTML = "";
        });
      }
    })
    .catch((error) => {
      console.error("Catch Error:", error);
    });
}

sameAddressCheckbox.addEventListener("change", function () {
  const shippingInfo = document.querySelector(".shipping-info");

  if (this.checked) {
    shippingInfo.style.display = "none";
  } else {
    shippingInfo.style.display = "block";
  }
});
