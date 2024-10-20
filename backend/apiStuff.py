import requests
import json
import geocoder
import math
from calculations import get_bussing_time, get_walking_time

# Dictionary of key locations on campus with their respective latitude and longitude coordinates
endCoordinates = {
    "Dreese Lab": (40.00224929496891, -83.01569116990318), 
    "Raney House": (40.005443412487615, -83.01009563632141), 
    "Ohio Union": (39.9976525575847, -83.00896671056906), 
    "Animal Science Building": (40.0036182750196, -83.02840914819784) 
}

# Function to retrieve bus route information from the OSU API
def get_bus_routes():
    url = "https://content.osu.edu/v2/bus/routes/CC"  # API endpoint for bus routes
    response = requests.get(url)  # Send GET request to the API
    
    # Check if the response was successful (status code 200)
    if response.status_code == 200:
        return response.json()  # Return the bus routes as JSON
    else:
        response.raise_for_status()  # Raise an error if request was not successful

# Main section to get and handle bus route data
if __name__ == "__main__":
    try:
        bus_routes = get_bus_routes()  # Fetch bus route data
        # Uncomment below to print bus routes
        # print(bus_routes)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")  # Print error if the API request fails

# Function to get information about the current bus vehicles
def get_bus_info():
    url = "https://content.osu.edu/v2/bus/routes/CC/vehicles"  # API endpoint for bus vehicle information
    response = requests.get(url)  # Send GET request to the API
    
    # Check if the response was successful (status code 200)
    if response.status_code == 200:
        return response.json()  # Return the bus information as JSON
    else:
        response.raise_for_status()  # Raise an error if request was not successful

# Main section to get and handle bus info data
if __name__ == "__main__":
    try:
        bus_routes = get_bus_info()  # Fetch bus vehicle data
        # Uncomment below to print bus routes
        # print(bus_routes)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")  # Print error if the API request fails

# Function to get current GPS coordinates based on IP address using geocoder
def get_current_gps_coordinates():
    g = geocoder.ip('me')  # Use geocoder to get location from the IP address
    if g.latlng is not None:  # Check if lat/long coordinates are available
        return g.latlng  # Return the latitude and longitude
    else:
        return None  # Return None if coordinates could not be found

# Main section to retrieve and display current GPS coordinates
if __name__ == "__main__":
    coordinates = get_current_gps_coordinates()
    if coordinates is not None:
        latitude, longitude = coordinates
        print(f"Your current GPS coordinates are:")  # Display current location coordinates
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
    else:
        print("Unable to retrieve your GPS coordinates.")  # Error message if coordinates are not found

# Function to find the closest bus stops to the user's current location
def get_closest_bus_stops(lat, lon):
    url = "https://content.osu.edu/v2/bus/routes/CC"  # API endpoint for bus stops
    response = requests.get(url)  # Send GET request to the API
    
    # Check if the response was successful (status code 200)
    if response.status_code == 200:
        bus_stops = response.json()  # Parse the response as JSON
        closest_stops = []
        
        # Loop through the list of bus stops and calculate the distance to each
        for stop in bus_stops['data']["stops"]:
            stop_lat = stop['latitude']
            stop_lon = stop['longitude']
            stop_name = stop['name']
            distance = math.sqrt((lat - stop_lat) ** 2 + (lon - stop_lon) ** 2)  # Calculate Euclidean distance
            
            pair = {"name": stop_name, "distance": distance, "latitude": stop_lat, "longitude": stop_lon}
            closest_stops.append(pair)  # Append stop details to the list of closest stops
        
        print(closest_stops)
        # Sort the stops by distance (smallest distance first)
        closest_stops.sort(key=lambda x: x['distance'])
        print("Now sorted:")
        print(closest_stops)
        
        # If stops are available, return the closest one
        if closest_stops:
            first_stop = closest_stops[0]
            first_lat = first_stop['latitude']
            first_lon = first_stop['longitude']
            print(f"First stop latitude: {first_lat}, longitude: {first_lon}")
            
            # Calculate the walking time to the closest stop
            timeWalk = get_walking_time(lat, lon, first_lat, first_lon)
            nameAndTime = {"name": first_stop['name'], "time": timeWalk, "latitude": first_lat, "longitude": first_lon}
            return nameAndTime
    else:
        response.raise_for_status()  # Raise an error if the request failed

# Get current GPS coordinates and find the closest bus stops
lat, lon = get_current_gps_coordinates()
allstops = get_closest_bus_stops(lat, lon)  # Find closest bus stops to the current location
print(allstops)

# Function to calculate total bus time, including time to walk to and from bus stops
def add_bus_times(lat, lon, lat2, lon2): 
    firstStop = get_closest_bus_stops(lat, lon)  # Get the first bus stop near current location
    print(f"firstStop: {firstStop}")
    
    lastStop = get_closest_bus_stops(lat2, lon2)  # Get the bus stop near the destination
    print(f"lastStop: {lastStop}")
    
    # Calculate bussing time between two stops
    bussingTime = get_bussing_time(firstStop['latitude'], firstStop['longitude'], lastStop['latitude'], lastStop['longitude'])
    
    # Print out time details
    print(f"firstStop: {firstStop['time']}")
    print(f"lastStop: {lastStop['time']}")
    print(f"bussTime: {bussingTime}")
    
    # Calculate the total bus time in seconds
    totalBusTime = firstStop['time'] + lastStop['time'] + bussingTime
    print(f"Bussing total time in seconds: {totalBusTime}")
    return totalBusTime

# Get current GPS coordinates and calculate total bus times to a specific destination
latitude, longitude = get_current_gps_coordinates()
print(f"Your current GPS coordinates are:", latitude, longitude)
busTimes = add_bus_times(latitude, longitude, 40.00251570565206, -83.01597557699893)  # Example destination

# Function to calculate total walking time between two locations
def get_total_walking_time(lat1, lon1, lat2, lon2):
    return get_walking_time(lat1, lon1, lat2, lon2)

# Compare walking time and bus time, and determine the fastest method
walkingTime = get_total_walking_time(latitude, longitude, 40.00251570565206, -83.01597557699893)
if walkingTime < busTimes:
    shortest = walkingTime
    method = "walking"  # Walking is faster
else:
    shortest = busTimes
    method = "bus"  # Bus is faster

# Print out the shortest travel time and method
print(f"The shortest time is {shortest} by {method}.")
