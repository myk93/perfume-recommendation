let perfumes = [];

fetch('New_Data_set.json')
    .then(response => response.json())
    .then(data => {
        perfumes = data;
        populateDropdowns();
    })
    .catch(
        fetch('static/New_Data_set.json')
    .then(response => response.json())
    .then(data => {
        perfumes = data;
        populateDropdowns();
    })
    .catch(
        error => console.error('Error loading JSON data:', error)
    )
    );

function populateDropdowns() {
    const familyDropdown = document.getElementById("family");
    const subfamilyDropdown = document.getElementById("subfamily");

    const families = [...new Set(perfumes.map(p => p.data.family))];
    const subfamilies = [...new Set(perfumes.map(p => p.data.subfamily))];

    families.forEach(family => {
        const option = document.createElement("option");
        option.value = family;
        option.textContent = family;
        familyDropdown.appendChild(option);
    });

    subfamilies.forEach(subfamily => {
        const option = document.createElement("option");
        option.value = subfamily;
        option.textContent = subfamily;
        subfamilyDropdown.appendChild(option);
    });

    const priceSlider = document.getElementById("price");
    const priceValue = document.getElementById("price-value");
    priceSlider.oninput = function() {
        priceValue.textContent = this.value;
    };
}

function recommendPerfume() {
    const userCollection = JSON.parse(localStorage.getItem('userCollection')) || [];

    fetch('http://127.0.0.1:5000/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ collection: userCollection })
    })
        .then(response => response.json())
        .then(data => displayPerfumeDetails(data))
        .catch(error => console.error('Error:', error));
}

function displayPerfumeDetails(perfumes) {
    const perfumeDetailsDiv = document.getElementById('perfume-details');
    perfumeDetailsDiv.innerHTML = "";

    if (perfumes.length > 0) {
        perfumes.forEach(perfume => {
            perfumeDetailsDiv.innerHTML += `
        <h2>${perfume.name || 'N/A'}</h2>
        <p><strong>Family:</strong> ${perfume.data.family }</p>
        <p><strong>Subfamily:</strong> ${perfume.data.subfamily || 'N/A'}</p>
        <p><strong>Price:</strong> ${perfume.data.price || 'N/A'}</p>
        <p><strong>Gender:</strong> ${perfume.data.gender || 'N/A'}</p>
        <p><strong>Year:</strong> ${perfume.data.year || 'N/A'}</p>
        <p><strong>Origin:</strong> ${perfume.data.origin || 'N/A'}</p>
        <p><strong>Description:</strong> ${perfume.data.description || 'N/A'}</p>
        <p><strong>Ingredients:</strong> ${Array.isArray(perfume.data.ingredients) ? perfume.data.ingredients.join(", ") : 'N/A'}</p>
        <p><strong>Concept:</strong> ${Array.isArray(perfume.data.concept) ? perfume.data.concept.join(", ") : 'N/A'}</p>
        <a href="${perfume.webPage || '#'}" target="_blank">More details</a>
    `;
        });
    } else {
        perfumeDetailsDiv.innerHTML = "<p>No perfumes found with the selected criteria.</p>";
    }
}

