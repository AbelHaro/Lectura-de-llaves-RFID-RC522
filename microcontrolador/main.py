import bluetooth  # Bluetooth module
from ble.ble_simple_peripheral import BLESimplePeripheral  # BLE module
import time
import wifi_connect as wifi
import data_sending_api as sender
import sensor
import led_control as led
import ubidots

# Initialize Bluetooth Low Energy (BLE) interface and Simple Peripheral
ble = bluetooth.BLE()
sp = BLESimplePeripheral(ble, name="Pico WH")

# Default mode for RFID sensor operation
MODE = 'ADD_USER_REGISTER'  # Default mode is to add user registration

def on_rx(data):
    """
    Callback function for receiving data from BLE.

    Parameters:
        data (bytes): Received data as bytes.

    Global Variables Modified:
        MODE (str): Updated mode based on received data.
    """
    global MODE  # Access global variable MODE within the function
    print("Data received:", data)

    # Update mode based on received data
    if data == b'ADD_USER_REGISTER\r\n':
        MODE = 'ADD_USER_REGISTER'
    elif data == b'ADD_TIME_REGISTRY\r\n':
        MODE = 'ADD_TIME_REGISTRY'


if __name__ == '__main__':
    # Connect to WiFi
    wifi.connect()

    try:    
        while True:
            if sp.is_connected():
                sp.on_write(on_rx)  # Register callback for BLE data reception
            # Read UID from sensor
            uid = sensor.read_sensor()
            
            # Determine mode and call appropriate API
            if MODE == 'ADD_USER_REGISTER':
                response = sender.add_user_register(uid)  # Call API to add user registration
            elif MODE == 'ADD_TIME_REGISTRY':
                response = sender.add_time_registry(uid)  # Call API to add time registry
            else:
                print('Error: Invalid mode')
                raise Exception('Invalid mode detected')  # Raise an exception for invalid mode
            
            # Blink LED based on API response status
            led.blink_led(response['api_status'])
            time.sleep(1)
    except KeyboardInterrupt:
        print('Programa abortado con CTRL+C desde main.py')  # Handle keyboard interrupt
    
        

    



