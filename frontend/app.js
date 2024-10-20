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

// Function to get the route to the selected destination
function getRoute() {
    const destination = document.getElementById('location-input').value;
    let destinationCoords = {
        "Dreese Lab": { lat: 40.00224929496891, lon: -83.01569116990318 },
        "Raney House": { lat: 40.005443412487615, lon: -83.01009563632141 },
        "Ohio Union": { lat: 39.9976525575847, lon: -83.00896671056906 },
        "Animal Science Building": { lat: 40.0036182750196, lon: -83.02840914819784 }
    };

    if (destinationCoords[destination]) {
        const { lat, lon } = destinationCoords[destination];

        if (destination === "Dreese Lab") {
            document.getElementById('route-display').innerText = `The shortest route to Dreese Lab is by walking taking 15 minutes.`;
        } else if (destination === "Raney House") {
            document.getElementById('route-display').innerText = `The shortest route to Raney House is by walking taking 14 minutes.`;
        } else if (destination === "Ohio Union") {
            document.getElementById('route-display').innerText = `The shortest route to Ohio Union is by walking taking 2 minutes.`;
        } else if (destination === "Animal Science Building") {
            document.getElementById('route-display').innerText = `The shortest route to Animal Science Building is by walking taking 32 minutes.`;
        } else {
            alert("Invalid destination selected.");
        }
        }
}

// Function to update bus capacity
function updateBusCapacity() {
    fetch('/api/message')
        .then(response => response.json())
        .then(data => {
            if (data.percentage_full > 100) {
                const spotsOver = Math.abs(data.spots_left); // Get the number of spots over capacity
                document.getElementById('people-count').textContent = `${spotsOver} spots over capacity!`;
                document.getElementById('overCapacity').classList.remove('hidden');
            } else {
                document.getElementById('people-count').textContent = `${data.percentage_full}% full, ${data.spots_left} spots left`;
                document.getElementById('overCapacity').classList.add('hidden');
            }
        })
        .catch(error => console.error('Error fetching bus capacity:', error));
}


// Call the function to get the current location and other data when the page loads
window.onload = function() {
    initMap(); // Get location from the browser and send to the server
    fetchLocationFromServer(); // Fetch location from the server and display
    updateBusCapacity(); // Fetch and display bus capacity

    setInterval(updateBusCapacity, 500); // Update bus capacity every 500ms
};
