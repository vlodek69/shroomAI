document.getElementById('uploadForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission

    const formData = new FormData(this);

    fetch('/prediction', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => { throw new Error(errorData.error); });
        }
        return response.json();
    })
    .then(data => {
        console.log("Data received:", data);

        document.getElementById('result').innerHTML = `
            <p>${data.name || 'No name available'}</p>
            <p><small>With probability of ${data.probability}%</small></p>
            <a href="https://en.wikipedia.org" target="_blank">
                <img src="${data.image}" alt="mushroom_image_x512.png" class="img-fluid" style="border-radius: 25%">
            </a>
            <p style="padding-top: 10px">${data.description || 'No description available'}</p>
        `;
    })
    .catch(error => {
        document.getElementById('result').innerHTML = `<p class="pointy" style="color: red;">${error.message}</p>`;
    });
});
