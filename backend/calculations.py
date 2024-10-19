import requests
from dotenv import load_dotenv
import os
load_dotenv()
MAPS_API_KEY = os.getenv("MAPS_API_KEY")
def get_walking_time(lat1, lon1, lat2, lon2, api_key):
    origin = f"{lat1},{lon1}"
    destination = f"{lat2},{lon2}"
    
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&mode=walking&key={api_key}"
    
    response = requests.get(url)
    data = response.json()
    
    if 'routes' in data and len(data['routes']) > 0:
        walking_time = data['routes'][0]['legs'][0]['duration']['value']  # Time in seconds
        print("Walking time in seconds: ", walking_time/60)
        return walking_time
    else:
        print("Error: Unable to get walking time")
        return None


get_walking_time(39.9612, -82.9988, 39.99781000000, -83.009831, MAPS_API_KEY)  # Example usage: calculate distance between two points