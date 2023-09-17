
let subscribeForm = document.getElementById('subscribe-form')
subscribeForm.addEventListener('submit', async function (event) {
    event.preventDefault()
    let email = document.getElementById('subscribe-email').value
    fetch('https://localhost:8000/api/newsletter/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': subscribeForm.csrfmiddlewaretoken.value
        },
        body: JSON.stringify({
            'email': email,
        })
    })
        .then(response => {
            if (response.ok) {
                subscribeForm.innerHTML = `<h4>Great! Thanks for subscribing to our weekly newsletter! We look forward to staying in touch. </h4>`
            }
            else {
                alert("Something went wrong! Please try again later.");
            }
        })
})
