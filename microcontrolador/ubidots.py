import ujson  # Module for handling JSON data
import urequests  # Module for making HTTP requests

# Constants for Ubidots API
URL_UBIDOTS = 'http://industrial.api.ubidots.com/api/v1.6/devices/controlador-de-acceso/'
TOKEN = 'BBUS-hOoHdkn7dj0w0q6xrOYD0hAwAVkwLW'

def add_user_register(uid):
    """
    Sends an HTTP POST request to Ubidots API to add a user registration.

    Parameters:
        uid (str): The UID (User ID) of the user to register.

    Returns:
        int: HTTP status code of the request.
    """
    data = {
        'add_user_register': {
            'value': 1,
            'context': {
                'UID': uid
            }
        }
    }
    request = urequests.post(
        URL_UBIDOTS,
        headers={'X-Auth-Token': TOKEN, 'Content-Type': 'application/json'},
        json=data
    )
    return request.status_code

def add_time_registry(uid, value):
    """
    Sends an HTTP POST request to Ubidots API to add a time registry.

    Parameters:
        uid (str): The UID (User ID) associated with the time registry.
        value (int): The value or data to be recorded in the time registry.

    Returns:
        int: HTTP status code of the request.
    """
    data = {
        'add_time_registry': {
            'value': value,
            'context': {
                'UID': uid
            }
        }
    }
    request = urequests.post(
        URL_UBIDOTS,
        headers={'X-Auth-Token': TOKEN, 'Content-Type': 'application/json'},
        json=data
    )
    return request.status_code