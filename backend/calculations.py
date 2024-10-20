import requests
from dotenv import load_dotenv
import os

load_dotenv()
MAPS_API_KEY = os.getenv("MAPS_API_KEY")

def get_walking_time(lat1, lon1, lat2, lon2):
    origin = f"{lat1},{lon1}"
    destination = f"{lat2},{lon2}"
    
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&mode=walking&key={MAPS_API_KEY}"
    
    response = requests.get(url)
    data = response.json()
    
    if 'routes' in data and len(data['routes']) > 0:
        walking_time = data['routes'][0]['legs'][0]['duration']['value']  # Time in seconds
        print("Walking time in seconds: ", walking_time)
        return walking_time
    else:
        print("Error: Unable to get walking time")
        return None

def get_bussing_time(lat1, lon1, lat2, lon2):
    origin = f"{lat1},{lon1}"
    destination = f"{lat2},{lon2}"
    
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&mode=driving&key={MAPS_API_KEY}"
    
    response = requests.get(url)
    data = response.json()
    
    if 'routes' in data and len(data['routes']) > 0:
        bussing_time = data['routes'][0]['legs'][0]['duration']['value']  # Time in seconds
        print("Bussing time in seconds: ", bussing_time)
        return bussing_time
    else:
        print("Error: Unable to get bussing time")
        return None

# Add this function to avoid the import error in main.py
def get_total_walking_time(lat1, lon1, lat2, lon2):
    return get_walking_time(lat1, lon1, lat2, lon2)
