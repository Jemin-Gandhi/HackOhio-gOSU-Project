import requests
import json
import geocoder

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
        print(bus_routes)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")



def printJsonObject(json_obj):
    print(json.dumps(json_obj, indent=4))
    try:
        bus_routes = get_bus_routes()
        printJsonObject(bus_routes)
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
        print(bus_routes)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")



        def printJsonObject(json_obj):
            print(json.dumps(json_obj, indent=4))

        try:
            bus_routes = get_bus_info()
            printJsonObject(bus_routes)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

def get_current_gps_coordinates():
    g = geocoder.ip('me')#this function is used to find the current information using our IP Add
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
            
            pair = {"name": stop_name, "distance": distance}
            closest_stops.append(pair)
        
        closest_stops.sort(key=lambda x: x['distance'])
        return closest_stops
    else:
        response.raise_for_status()