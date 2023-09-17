let subscribeForm = document.getElementById("subscribe-form");

subscribeForm.addEventListener("submit", async function (event) {
    event.preventDefault();
    let email = document.getElementById("subscribe-email").value;
  
    try {
      const response = await fetch("/api/newsletter/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": subscribeForm.csrfmiddlewaretoken.value,
        },
        body: JSON.stringify({
          email: email,
        }),
      });
  
      if (response.ok) {
        subscribeForm.innerHTML = `<h4 class="newsletter-text-success">Great! Thanks for subscribing to our weekly newsletter! We look forward to staying in touch.</h4>`;
        showSuccessToast("You've successfully subscribed to our newsletter. Thank you for joining us!");
      } else {
        const data = await response.json();
        let errorList = document.querySelector("#subscribe-form .errorlist");
  
        let html = "";
        for (let [key, value] of Object.entries(data)) {
          html += `<li class="error">${value}</li>`;
        }
        errorList.innerHTML = html;
      }
    } catch (error) {
      console.error("Error:", error);
    }
  });
  

// Toastify Message Function
function showSuccessToast(message) {
  Toastify({
    text: message,
    duration: 1500,
    close: false,
    gravity: "top",
    position: "right",
    style: {
      background: "#4CAF50",
      color: "#fff",
      borderRadius: "5px",
      padding: "10px 20px",
      fontSize: "16px",
      opacity: 0.9,
    },
  }).showToast();
}
