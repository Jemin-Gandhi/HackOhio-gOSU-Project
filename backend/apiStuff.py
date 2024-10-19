import requests
import json

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