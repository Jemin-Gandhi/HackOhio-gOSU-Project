import requests
import json
import geocoder

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
        print("Unable to retrieve your GPS coordinates.")