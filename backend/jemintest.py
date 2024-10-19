import requests
import json
import geocoder
import math

def get_closest_bus_stops(lat, lon):
    url = "https://content.osu.edu/v2/bus/routes/CC"
    response = requests.get(url)
    
    if response.status_code == 200:
        bus_stops = response.json()
        closest_stops = []
        for stop in bus_stops['data']["stops"]:
            stop_lat = stop['latitude']
            stop_lon = stop['longitude']
            stop_name = stop['name']
            distance = math.sqrt((lat - stop_lat) ** 2 + (lon - stop_lon) ** 2)
            
            pair = {"name": stop_name, "distance": distance}
            closest_stops.append(pair)
        
        closest_stops.sort(key=lambda x: x['distance'])
        return closest_stops
    else:
        response.raise_for_status()


lat, lon = 39.997618, -83.008567

allstops = get_closest_bus_stops(lat, lon)  # Example usage: find the closest bus stops to a given location
print(allstops)


