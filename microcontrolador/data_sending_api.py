import time  # Standard Python time module
import ujson  # Module for handling JSON data
import urequests as requests  # Module for making HTTP requests (alias for urequests)

URL = 'http://192.168.1.2:8888/api/'
URL_add_user_register = URL + 'user_register/add'
URL_add_time_registry = URL + 'time_registry/add'
URL_get_user_registered_by_uid = URL + 'user_register'

def get_local_time() -> str:
    """
    Returns the timestamp formatted.
    """
    local_time = time.localtime()
    formatted_time = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
    local_time[0],  # year
    local_time[1],  # month
    local_time[2],  # day
    local_time[3],  # hour
    local_time[4],  # minute
    local_time[5]   # second
    )
    return str(formatted_time)

def add_user_register(uid):
    """
    Adds the user to the database using a POST request.
    
    Parameters:
        uid (str): The UID (Unique ID) of the user to be registered.
    
    Returns:
        dict: A dictionary containing the response message from the server.
    """
     
    data_sending = {
        "UID": uid,
        "user_creation_tstamp": get_local_time()
    }
    
    response = requests.post(URL_add_user_register, headers={'Content-Type': 'application/json'}, data=ujson.dumps(data_sending))
    return ujson.loads(response.content)
    
def add_time_registry(uid):
    """
    Adds the time registry to the database using a POST request.
    
    Parameters:
        uid (str): The UID (Unique ID) of the user to be registered.
    
    Returns:
        dict: A dictionary containing the response message from the server.
    """
    data_sending = {
        "UID": uid,
        "user_registry_tstamp": get_local_time()
    }
    
    response = requests.post(URL_add_time_registry, headers={'Content-Type': 'application/json'}, data=ujson.dumps(data_sending))
    return ujson.loads(response.content)

def get_user_registered_by_uid(uid):
    """
    Retrieves user registration details from the server based on UID using a GET request.
    
    Parameters:
        uid (str): The UID (Unique ID) of the user to be registered.
    
    Returns:
        dict: A dictionary containing the response message from the server.
    """
    response = requests.get(URL_get_user_registered_by_uid + '/%s'.format(uid))
    return ujson.loads(response.content)