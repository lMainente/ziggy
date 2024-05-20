from tuyapy import TuyaApi
import json
import time


cached_api = None
last_auth_time = 0

def load_credentials(filename='config.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Credentials file not found.")
        return None

def save_credentials(credentials, filename='config.json'):
    with open(filename, 'w') as file:
        json.dump(credentials, file)

def authenticate_tuya():
    global cached_api, last_auth_time
    
    if cached_api and time.time() - last_auth_time < 180:
        return cached_api
    
    credentials = load_credentials()
    if credentials is None:
        print("Credentials not found. Please provide account details.")
        return None
    
    api = TuyaApi()
    api.init(credentials["username"], credentials["password"], credentials["country_code"], credentials["application"])
    
    cached_api = api
    last_auth_time = time.time()
    
    return api


def turn_off_light(light):
    light.turn_off()
    print(f"Turned off {light.name()}")

def turn_on_light(light):
    light.turn_on()
    print(f"Turned on {light.name()}")

def get_available_lights(api):
    device_ids = api.get_all_devices()
    lights = [device for device in device_ids if device.obj_type == 'light']
    
    return lights

def toggle_all_lights(api, action):
    lights = get_available_lights(api)
    
    if action.lower() == 'on':
        for light in lights:
            turn_on_light(light)
        print("All lights turned on.")
    elif action.lower() == 'off':
        for light in lights:
            turn_off_light(light)
        print("All lights turned off.")
    else:
        print("Invalid action. Please enter 'on' or 'off'.")

if __name__ == "__main__":
    api = authenticate_tuya()
    if api:
        choice = input("Enter 'on' to turn on all lights or 'off' to turn off all lights: ")
        toggle_all_lights(api, choice)
