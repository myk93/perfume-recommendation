let perfumes = [];
let userCollection = JSON.parse(localStorage.getItem('userCollection')) || [];

fetch('New_Data_set.json')
    .then(response => response.json())
    .then(data => {
        perfumes = data;
        updateCollectionList();
    })
    .catch(error => console.error('Error loading JSON data:', error));

function fuzzySearch(query, items) {
    const lowerQuery = query.toLowerCase();
    return items.filter(item => item.name.toLowerCase().includes(lowerQuery));
}

document.getElementById('search').addEventListener('input', function() {
    const query = this.value;
    const suggestionsDiv = document.getElementById('autocomplete-suggestions');
    suggestionsDiv.innerHTML = "";

    if (query.length > 0) {
        const suggestions = fuzzySearch(query, perfumes);
        suggestions.forEach(perfume => {
            const suggestionDiv = document.createElement('div');
            suggestionDiv.className = 'autocomplete-suggestion';
            suggestionDiv.textContent = perfume.name;
            suggestionDiv.onclick = function() {
                addPerfumeToCollection(perfume);
                document.getElementById('search').value = "";
                suggestionsDiv.innerHTML = "";
            };
            suggestionsDiv.appendChild(suggestionDiv);
        });
    }
});

function addPerfumeToCollection(perfume) {
    if (!userCollection.some(p => p.name === perfume.name)) {
        userCollection.push(perfume);
        localStorage.setItem('userCollection', JSON.stringify(userCollection));
        updateCollectionList();
    }
}

function updateCollectionList() {
    const collectionList = document.getElementById('collection-list');
    collectionList.innerHTML = "";

    userCollection.forEach((perfume, index) => {
        const li = document.createElement('li');
        li.textContent = perfume.name;

        li.onclick = function() {
            displayPerfumeDetails(perfume);
        };

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.onclick = function(event) {
            event.stopPropagation(); // Prevent the click from triggering the display
            deletePerfumeFromCollection(index);
        };

        li.appendChild(deleteButton);
        collectionList.appendChild(li);
    });
}

function deletePerfumeFromCollection(index) {
    userCollection.splice(index, 1);
    localStorage.setItem('userCollection', JSON.stringify(userCollection));
    updateCollectionList();
    clearPerfumeDetails(); 
}

function displayPerfumeDetails(perfume) {
    const detailsDiv = document.getElementById('perfume-details');
    detailsDiv.style.display = 'block';
    detailsDiv.innerHTML = `
        <h2>${perfume.name}</h2>
        <p><strong>Family:</strong> ${perfume.data.family}</p>
        <p><strong>Subfamily:</strong> ${perfume.data.subfamily}</p>
        <p><strong>Price:</strong> ${perfume.data.price}</p>
        <p><strong>Gender:</strong> ${perfume.data.gender}</p>
        <p><strong>Year:</strong> ${perfume.data.year}</p>
        <p><strong>Origin:</strong> ${perfume.data.origin}</p>
        <p><strong>Description:</strong> ${perfume.data.description}</p>
        <p><strong>Ingredients:</strong> ${perfume.data.ingredients.join(", ")}</p>
        <p><strong>Concept:</strong> ${perfume.data.concept.join(", ")}</p>
        <a href="${perfume.webPage}" target="_blank">More details</a>
    `;
}

function clearPerfumeDetails() {
    const detailsDiv = document.getElementById('perfume-details');
    detailsDiv.style.display = 'none';
    detailsDiv.innerHTML = '';
}
