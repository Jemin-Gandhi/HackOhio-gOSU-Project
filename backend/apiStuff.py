import requests
import json
import geocoder
import math
from calculations import get_bussing_time, get_walking_time
import os
from dotenv import load_dotenv
load_dotenv()
MAPS_API_KEY = os.getenv("MAPS_API_KEY")

endCoordinates = {
    "Dreese Lab": (40.00224929496891, -83.01569116990318), 
    "Raney House": (40.005443412487615, -83.01009563632141), 
    "Ohio Union": (39.9976525575847, -83.00896671056906), 
    "Animal Science Building": (40.0036182750196, -83.02840914819784) 
}

def get_bus_routes():
    url = "https://content.osu.edu/v2/bus/routes/CC"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

if __name__ == "__main__":
    try:
        bus_routes = get_bus_routes()
        #print(bus_routes)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")




def get_bus_info():
    url = "https://content.osu.edu/v2/bus/routes/CC/vehicles"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

if __name__ == "__main__":
    try:
        bus_routes = get_bus_info()
        #print(bus_routes)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

#def get_current_gps_coordinates():
 #   g = geocoder.ip('me')#this function is used to find the current information using our IP Add
  #  if g.latlng is not None: #g.latlng tells if the coordiates are found or not
   #     return g.latlng
    #else:
      #  return None

def get_current_gps_coordinates():
    place_to_go = "Udf 12th"
    address = place_to_go + " Ohio State University"
    g = geocoder.google(address, method='places', key = MAPS_API_KEY)#this function is used to find the current information using our IP Add
    if g.latlng is not None: #g.latlng tells if the coordiates are found or not
        return g.latlng
    else:
        return None

if __name__ == "__main__":
    coordinates = get_current_gps_coordinates()
    if coordinates is not None:
        latitude, longitude = coordinates
        print(f"Your current GPS coordinates are:")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
    else:
        print("Unable to retrieve your GPS coordinates.")\


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
            
            pair = {"name": stop_name, "distance": distance, "latitude": stop_lat, "longitude": stop_lon}
            closest_stops.append(pair)
        #print(closest_stops)
        closest_stops.sort(key=lambda x: x['distance'])
        #print("Now sorted:")
        #print(closest_stops)
        if closest_stops:
            first_stop = closest_stops[0]
            first_lat = first_stop['latitude']
            first_lon = first_stop['longitude']
            print(f"First stop latitude: {first_lat}, longitude: {first_lon}")
            timeWalk = get_walking_time(lat, lon, first_lat, first_lon)
            nameAndTime = {"name": first_stop['name'], "time": timeWalk, "latitude": first_lat, "longitude": first_lon}
            return nameAndTime
    else:
        response.raise_for_status()

#lat, lon = get_current_gps_coordinates()

#allstops = get_closest_bus_stops(lat, lon)  # Example usage: find the closest bus stops to a given location
#print(allstops)

def add_bus_times(lat, lon, lat2, lon2): 
    firstStop = get_closest_bus_stops(lat, lon)
    print(f"firstStop: {firstStop}")
    lastStop = get_closest_bus_stops(lat2, lon2) #THIS IS WHERE THE USER CHOOSES ENDING DESTINATION
    print(f"lastStop: {lastStop}")
    bussingTime = get_bussing_time(firstStop['latitude'], firstStop['longitude'], lastStop['latitude'], lastStop['longitude'])
    print(f"firstStop: {firstStop['time']}")
    print(f"lastStop: {lastStop['time']}")
    print(f"bussTime: {bussingTime}")
    totalBusTime = firstStop['time'] + lastStop['time'] + bussingTime
    print(f"Bussing total time in seconds: {totalBusTime}")
    return totalBusTime

#latitude, longitude = get_current_gps_coordinates()
#print(f"Your current GPS coordinates are:", latitude, longitude)
#busTimes = add_bus_times(latitude, longitude, 40.00251570565206, -83.01597557699893) # Example usage: calculate total time to bus from current location to destination

def get_total_walking_time(lat1, lon1, lat2, lon2):
    return get_walking_time(lat1, lon1, lat2, lon2)
     
print ("testing")
latitude, longitude = get_current_gps_coordinates()
#latitude, longitude = 40.001830132172216, -83.01082794650411 #hardcoded coordinates for testing, stillman rn.
lat2, long2 = endCoordinates["Dreese Lab"]
print(f"Your current GPS coordinates are:", latitude, longitude)
busTimes = add_bus_times(latitude, longitude, lat2, long2) # Example usage: calculate total time to bus from current location to destination
walkingTime = get_total_walking_time(latitude, longitude, 40.00251570565206, -83.01597557699893)
if walkingTime < busTimes:
    shortest = walkingTime
    method = "walking"
else:
    shortest = busTimes
    method = "bus"
print(f"The shortest time is {shortest} seconds by {method}.")
