//Fetching data from a Sonar API once I have access

document.addEventListener('DOMContentLoaded', function() {
    // Button to trigger data fetching
    const fetchButton = document.getElementById('fetch-data');
    const resultContainer = document.getElementById('result-container');

    fetchButton.addEventListener('click', function() {
        // Fetch data from a mock API (replace URL with Sonar API endpoint)
        fetch('https://api.mocki.io/v1/ce3c8b64') // Mock API URL
            .then(response => response.json())
            .then(data => {
                // Display fetched data in the result container
                resultContainer.innerHTML = `
                    <h3>Fetched Data:</h3>
                    <p><strong>Title:</strong> ${data.title}</p>
                    <p><strong>Description:</strong> ${data.description}</p>
                `;
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                resultContainer.innerHTML = '<p>Error fetching data, please try again later.</p>';
            });
    });
});
