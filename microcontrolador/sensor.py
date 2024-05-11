import bluetooth  # Bluetooth module
from ble.ble_simple_peripheral import BLESimplePeripheral  # BLE module
from lib.mfrc522.mfrc522 import MFRC522  # RFID reader module
import time  # Time-related functions
import data_sending_api as sender  # Custom API module for data sending

# Initialize Bluetooth Low Energy (BLE) interface and Simple Peripheral
ble = bluetooth.BLE()
sp = BLESimplePeripheral(ble, name="Pico WH")

# Default mode for RFID sensor operation
MODE = 'ADD_USER_REGISTER'  # Default mode is to add user registration

def read_sensor() -> str:
    """
    Function to read RFID sensor and perform actions based on the received data.

    Returns:
        str: Response message from the data sending API.
    """
    # Initialize the MFRC522 RFID reader
    lector = MFRC522(spi_id=0, sck=2, miso=4, mosi=3, cs=1, rst=0)

    print("RFID sensor active...\n")

    try:
        i = 0
        while True:
            # Check if BLE connection is established
            if sp.is_connected():
                sp.on_write(on_rx)  # Register callback for BLE data reception

            i = i + 1
            print(str(i) + ' ' + MODE)  # Print iteration count and current mode

            lector.init()  # Initialize the RFID reader
            (stat, tag_type) = lector.request(lector.REQIDL)  # Request tag detection

            if stat == lector.OK:
                (stat, uid) = lector.SelectTagSN()  # Select detected tag
                if stat == lector.OK:
                    # Convert UID bytes to integer for identification
                    identificador = int.from_bytes(bytes(uid), "little", False)
                    print("UID: " + str(identificador))  # Print detected UID

                    uid = str(identificador)  # Convert UID to string

                    # Perform action based on the current mode (MODE)
                    if MODE == 'ADD_USER_REGISTER':
                        return sender.add_user_register(uid)  # Call API to add user registration
                    elif MODE == 'ADD_TIME_REGISTRY':
                        return sender.add_time_registry(uid)  # Call API to add time registry
                    else:
                        print('Error: Invalid mode')
                        return False  # Return False if invalid mode detected

            time.sleep(1)  # Sleep for 1 second between iterations

    except KeyboardInterrupt:
        print("Program terminated with CTRL+C from sensor.py")  # Handle keyboard interrupt

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