// Parent Comment Form
const blogReviewForm = document.querySelector("#blog-review-form");
const errorList = document.querySelector("#blog-review-form .errorlist");

blogReviewForm.addEventListener("submit", function (event) {
  event.preventDefault();

  const reviewData = {
    blog: blogReviewForm.blog_id.value,
    subject: blogReviewForm.subject.value,
    comment: blogReviewForm.comment.value,
  };

  if (!isAuthenticated) {
    reviewData.full_name = blogReviewForm.full_name.value;
    reviewData.email = blogReviewForm.email.value;
  }

  fetch("/api/blog-reviews/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": blogReviewForm.csrfmiddlewaretoken.value,
    },
    body: JSON.stringify(reviewData),
  })
    .then((response) => {
      if (response.ok) {
        blogReviewForm.reset();
        errorList.innerHTML = "";

        showSuccessToast("Your comment has been successfully saved.");

        setTimeout(function () {
          location.reload();
      }, 600);

      } else {
        response.json().then((data) => {
          console.error("Error code:", response.status);
          console.error("Error message:", data);

          html = "";
          for (let [key, value] of Object.entries(data)) {
            html += `<li class="error">${key.replace(/_/g, ' ').toUpperCase()}: ${value}</li>`;
          }
          errorList.innerHTML = html;
        });
      }
    })
    .catch((error) => {
      console.error("Catch Error:", error);
    });
});

// Reply Buttons
const replyButtons = document.querySelectorAll(".reply-button");

replyButtons.forEach((button) => {
  button.addEventListener("click", (event) => {
    const parentComment = event.target.closest(".media");
    const replyForm = parentComment.querySelector(".reply-form");

    if (replyForm.style.display === "none" || replyForm.style.display === "") {
      replyForm.style.display = "block";
    } else {
      replyForm.style.display = "none";
    }
  });
});

// Reply Forms
const replyForms = document.querySelectorAll(".reply-form");

replyForms.forEach((form) => {
  form.addEventListener("submit", (event) => {
    event.preventDefault();

    const replyData = {
      blog: form.blog_id.value,
      parent: form.parent_id.value,
      subject: form.subject.value,
      comment: form.comment.value,
    };

    if (!isAuthenticated) {
      replyData.full_name = form.full_name.value;
      replyData.email = form.email.value;
    }

    fetch("/api/blog-reviews/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": form.csrfmiddlewaretoken.value,
      },
      body: JSON.stringify(replyData),
    })
      .then((response) => {
        if (response.ok) {
          let errorList = form.querySelector(".errorlist");
          form.reset();
          errorList.innerHTML = "";
          form.style.display = "none";

          showSuccessToast("Your reply has been successfully saved.");
  
          setTimeout(function () {
            location.reload();
        }, 600);

        } else {
          response.json().then((data) => {
            console.error("Error code:", response.status);
            console.error("Error message:", data);

            let errorList = form.querySelector(".errorlist");
            let html = "";
            for (let [key, value] of Object.entries(data)) {
              html += `<li class="error">${key.replace(/_/g, ' ').toUpperCase()}: ${value}</li>`;
            }
            errorList.innerHTML = html;
          });
        }
      })
      .catch((error) => {
        console.error("Catch Error:", error);
      });
  });
});


// Toastify Message Function
function showSuccessToast(message) {
  Toastify({
    text: message,
    duration: 400,
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