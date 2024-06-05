from lib.mfrc522.mfrc522 import MFRC522  # RFID reader module
import time  # Time-related functions

def read_sensor() -> str:
    """
    Function to read RFID sensor and perform actions based on the received data.

    Returns:
        str: UID from card or key readed.
    """
    # Initialize the MFRC522 RFID reader
    lector = MFRC522(spi_id=0, sck=2, miso=4, mosi=3, cs=1, rst=0)

    print("RFID sensor active...\n")

    try:
        while True:
            lector.init()  # Initialize the RFID reader
            (stat, tag_type) = lector.request(lector.REQIDL)  # Request tag detection

            if stat == lector.OK:
                (stat, uid) = lector.SelectTagSN()  # Select detected tag
                if stat == lector.OK:
                    # Convert UID bytes to integer for identification
                    identificador = int.from_bytes(bytes(uid), "little", False)
                    print("UID: " + str(identificador))  # Print detected UID

                    return str(identificador)  # Convert UID to string
                
            time.sleep(1)  # Sleep for 1 second between iterations

    except KeyboardInterrupt:
        print("Program terminated with CTRL+C from sensor.py")  # Handle keyboard interrupt
