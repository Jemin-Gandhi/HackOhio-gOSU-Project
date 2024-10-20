// Geolocation functions
function initMap() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        console.error("Geolocation is not supported by this browser.");
    }
}

function showPosition(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    document.getElementById('coords-display').innerText = `Latitude: ${lat}, Longitude: ${lon}`;

    // Send the coordinates to the Flask server
    fetch('/api/location', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ latitude: lat, longitude: lon })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Location data sent successfully:', data);
    })
    .catch((error) => {
        console.error('Error sending location data:', error);
    });
}

function showError(error) {
    switch (error.code) {
        case error.PERMISSION_DENIED:
            console.error("User denied the request for Geolocation.");
            break;
        case error.POSITION_UNAVAILABLE:
            console.error("Location information is unavailable.");
            break;
        case error.TIMEOUT:
            console.error("The request to get user location timed out.");
            break;
        case error.UNKNOWN_ERROR:
            console.error("An unknown error occurred.");
            break;
    }
}

// Function to get location data from Flask and display it
function fetchLocationFromServer() {
    fetch('/api/get-location')
    .then(response => response.json())
    .then(data => {
        if (data.latitude && data.longitude) {
            document.getElementById('coords-display').innerText = `Latitude: ${data.latitude}, Longitude: ${data.longitude}`;
        } else {
            document.getElementById('coords-display').innerText = "No location data available";
        }
    })
    .catch(error => {
        console.error('Error fetching location:', error);
        document.getElementById('coords-display').innerText = "Error fetching location data";
    });
}

// Call the function to get the current location when the page loads
window.onload = function() {
    initMap(); // Get location from the browser and send to the server
    fetchLocationFromServer(); // Fetch location from the server and display
};
