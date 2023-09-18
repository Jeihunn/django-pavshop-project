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
  });
});

// Delete Comment
const deleteButtons = document.querySelectorAll(".delete-button");

deleteButtons.forEach((button) => {
  button.addEventListener("click", (event) => {
    event.preventDefault();

    const confirmDelete = confirm(
      "Are you sure you want to delete this comment?"
    );

    if (confirmDelete) {
      const commentId = button.getAttribute("data-id");

      fetch(`/api/blog-review/${commentId}/`, {
        method: "DELETE",
        headers: {
          "X-CSRFToken": getCSRFToken(),
        },
      })
        .then((response) => {
          if (response.ok) {
            showSuccessToast("Comment deleted successfully!");

            setTimeout(function () {
              location.reload();
            }, 600);
          } else {
            response.json().then((data) => {
              console.error("Error code:", response.status);
              console.error("Error message:", data);
            });
          }
        })
        .catch((error) => {
          console.error("Catch Error:", error);
        });
    }
  });
});

// Edit Comment Form
const editForms = document.querySelectorAll(".edit-forms");

editForms.forEach((form) => {
  form.addEventListener("submit", (event) => {
    event.preventDefault();

    const commentId = form.getAttribute("data-id");
    const comment = document.getElementById(`comment-${commentId}`);

    const editData = {
      id: commentId,
      comment: form.comment.value,
    };

    fetch(`/api/blog-review/${commentId}/`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": form.csrfmiddlewaretoken.value,
      },
      body: JSON.stringify(editData),
    })
      .then((response) => {
        if (response.ok) {
          form.style.display = "none";
          comment.innerText = form.comment.value;
          comment.style.display = "block";

          showSuccessToast("Comment edited successfully!", 1500);
        } else {
          response.json().then((data) => {
            console.error("Error code:", response.status);
            console.error("Error message:", data);

            let errorList = form.querySelector(".errorlist");
            let html = "";
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
  });
});

// Toastify Message Function
function showSuccessToast(message, duration) {
  Toastify({
    text: message,
    duration: duration || 400,
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

// Function to retrieve the Django CSRF token from cookies
function getCSRFToken() {
  const cookieValue = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="));

  if (cookieValue) {
    return cookieValue.split("=")[1];
  } else {
    return null;
  }
}

// Reply Buttons
const replyButtons = document.querySelectorAll(".reply-button");

replyButtons.forEach((button) => {
  button.addEventListener("click", (event) => {
    const parentComment = event.target.closest(".media");
    const replyForm = parentComment.querySelector(".reply-form");

    const allEditForms = document.querySelectorAll('[id^="edit-form-"]');
    const allComments = document.querySelectorAll('[id^="comment-"]');
    const allReplyForms = document.querySelectorAll(".reply-form");
    console.log(allReplyForms);

    allEditForms.forEach((form) => {
      form.style.display = "none";
    });

    allComments.forEach((comment) => {
      comment.style.display = "block";
    });

    allReplyForms.forEach((form) => {
      if (form === replyForm) {
        if (
          replyForm.style.display === "none" ||
          replyForm.style.display === ""
        ) {
          replyForm.style.display = "block";
        } else {
          replyForm.style.display = "none";
        }
      } else {
        form.style.display = "none";
      }
    });
  });
});

// Edit Buttons
const editButtons = document.querySelectorAll(".edit-button");

editButtons.forEach((button) => {
  button.addEventListener("click", (event) => {
    const commentId = button.getAttribute("data-id");
    const editForm = document.querySelector(`#edit-form-${commentId}`);
    const comment = document.querySelector(`#comment-${commentId}`);
    console.log(comment);

    const allEditForms = document.querySelectorAll('[id^="edit-form-"]');
    const allComments = document.querySelectorAll('[id^="comment-"]');
    const allReplyForms = document.querySelectorAll(".reply-form");

    allReplyForms.forEach((form) => {
      form.style.display = "none";
    });

    editForm.style.display = "block";
    comment.style.display = "none";

    allEditForms.forEach((form) => {
      if (form !== editForm) {
        form.style.display = "none";
      }
    });

    allComments.forEach((commentF) => {
      if (commentF !== comment) {
        commentF.style.display = "block";
      }
    });
  });
});

// Cancel Buttons
const cancelButtons = document.querySelectorAll(".edit-cancel-button");

cancelButtons.forEach((button) => {
  button.addEventListener("click", (event) => {
    const commentId = button.getAttribute("data-id");
    const editForm = document.querySelector(`#edit-form-${commentId}`);
    const comment = document.querySelector(`#comment-${commentId}`);

    editForm.style.display = "none";
    comment.style.display = "block";
  });
});
