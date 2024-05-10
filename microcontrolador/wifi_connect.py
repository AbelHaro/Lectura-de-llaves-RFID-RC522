import network  # Module for network management
import time  # Module for time-related functions

# Wi-Fi credentials
ssid = ''  # SSID of the Wi-Fi network
password = ''  # Password of the Wi-Fi network

def connect():
    """
    Connects to a Wi-Fi network using the provided SSID and password.

    Raises:
        RuntimeError: If the network connection fails.

    Returns:
        network.WLAN: WLAN object representing the network connection.
    """
    wlan = network.WLAN(network.STA_IF)  # Create WLAN station interface
    wlan.active(True)  # Activate the WLAN interface

    # Attempt to connect to the Wi-Fi network
    wlan.connect(ssid, password)

    max_wait = 10  # Maximum wait time (in seconds) for the connection
    while max_wait > 0:
        if wlan.isconnected():
            break  # Exit loop if connected successfully
        max_wait -= 1
        #print('Waiting for connection...')
        time.sleep(1)  # Wait for 1 second before checking again

    if not wlan.isconnected():
        raise RuntimeError('Network connection failed')  # Raise error if connection fails
    else:
        #print('Connected!')
        status = wlan.ifconfig()  # Get network configuration
        print('IP Address:', status[0])  # Print IP address
        return wlan  # Return WLAN object representing the network connection
