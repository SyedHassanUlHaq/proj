document.getElementById("orderForm").addEventListener("submit", function(e) {
    e.preventDefault(); // prevent normal form submission

    const form = e.target;
    const formData = new FormData(form);

    fetch(form.action, {
        method: form.method,
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById("responseMessage").textContent = data;
        form.reset(); // clear form
    })
    .catch(error => {
        document.getElementById("responseMessage").textContent = "An error occurred: " + error;
    });
});
