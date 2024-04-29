import sqlite3
from flask import Flask, request, jsonify
import requests
from ignore.ubidots import URL_UBIDOTS, TOKEN_UBIDOTS

def connect_to_db():
    """
    Establishes a connection to the SQLite database.

    Returns:
        sqlite3.Connection: SQLite database connection object.
    """
    conn = sqlite3.connect('./database/database.db')
    
    return conn

def insert_random_data():
    """
    Inserts random data into the 'user_register' and 'time_registry' tables of the SQLite database.

    Returns:
        list: List of dictionaries representing the user registration data.
    """
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        cur.execute('''SELECT count(*) FROM user_register''')
        rows = cur.fetchall()
        if rows[0][0] == 0:
            insert_user_register({'UID': '1', 'user_creation_tstamp': '2021-06-15T13:45:30'})
            insert_user_register({'UID': '2', 'user_creation_tstamp': '2021-06-15T13:45:30'})
        cur.execute('''SELECT count(*) FROM time_registry''')
        rows = cur.fetchall()
        if rows[0][0] == 0:
            insert_time_registry({'user_registry_tstamp': '2021-06-15T13:45:30', 'UID': '1'})
            insert_time_registry({'user_registry_tstamp': '2021-06-15T13:45:31', 'UID': '2'})
        conn.commit()
    except:
        conn.rollback()
    finally:
        conn.close()
    return get_user_register()

def insert_user_register(user):
    """
    Inserts a new user registration record into the 'user_register' table and send it to Ubidots.

    Parameters:
        user (dict): Dictionary containing user information with keys:
                     - 'UID': Unique ID of the user.
                     - 'user_creation_tstamp': Timestamp of user creation.

    Returns:
        dict: Dictionary containing the status of the operation and error message (if any).
              Keys:
              - 'api_status': Boolean indicating the success of the operation.
              - 'error': Error message if an error occurred during the operation.v
              - 'ubidots_status': HTTP status code of the request to Ubidots.
              - 'UID': Unique ID of the user.
              - 'user_creation_tstamp': Timestamp of user creation.
    """
    inserted_user = {'api_status': False, 'error': None, 'ubidots_status': False, 'UID': None, 'user_creation_tstamp': None}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM user_register WHERE UID = ?", (user['UID'],))
        rows = cur.fetchall()
        if len(rows) > 0:
            inserted_user['error'] = "User already exists"
            return inserted_user
        
        cur.execute("INSERT INTO user_register (UID, user_creation_tstamp) VALUES (?, ?)",
                    (user['UID'], user['user_creation_tstamp']) )
        conn.commit()
        inserted_user.update(get_user_register_by_uid(user['UID']))
        ubidots_status = add_user_ubidots(user['UID'])
        if ubidots_status == 200:
            inserted_user['api_status'] = True
        else :
            inserted_user['error'] = "Error adding user to Ubidots"
            
        inserted_user['ubidots_status'] = ubidots_status
    except:
        conn.rollback()
    finally:
        conn.close()
        print(inserted_user)
    return inserted_user

def insert_time_registry(time_registry):
    """
    Inserts a new time registry record into the 'time_registry' table ans sends it to Ubidots.

    Parameters:
        time_registry (dict): Dictionary containing time registry information with keys:
                              - 'user_registry_tstamp': Timestamp of user registry.
                              - 'UID': Unique ID of the user associated with the time registry.

    Returns:
        dict: Dictionary containing the status of the operation and error message (if any).
              Keys:
              - 'api_status': Boolean indicating the success of the operation.
              - 'error': Error message if an error occurred during the operation.
              - 'ubidots_status': HTTP status code of the request to Ubidots.
              - 'user_registry_tstamp': Timestamp of user registry.
              - 'UID': Unique ID of the user associated with the time registry.
              - 'id': ID of the time registry record.
    """
    inserted_time_registry = {'api_status': False, 'error': None, 'ubidots_status': False, 'user_registry_tstamp': None, 'UID': None, 'id': None}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        #Check if user exists
        cur.execute("SELECT * FROM user_register WHERE UID = ?", (time_registry['UID'],))
        rows = cur.fetchall()
        if len(rows) == 0:
            inserted_time_registry['error'] = "User does not exist, please create it first."
            return inserted_time_registry
        
        #The user exists, insert the time_registry
        cur.execute("INSERT INTO time_registry (user_registry_tstamp, UID) VALUES (?, ?)",
                    (time_registry['user_registry_tstamp'], time_registry['UID']) )
        conn.commit()
        
        query = get_time_registry_by_uid(time_registry['UID'])
        inserted_time_registry.update(query[len(query)-1])
        inserted_time_registry['api_status'] = True
    except:
        conn().rollback()
    finally:
        conn.close()
        ubidots_status = add_time_registry_ubidots(time_registry['UID'], inserted_time_registry['api_status'])
        inserted_time_registry['ubidots_status'] = ubidots_status
    return inserted_time_registry

def get_user_register():
    """
    Retrieves all records from the 'user_register' table and converts them into dictionaries.

    Returns:
        list: A list of dictionaries representing the users registered.
              Each dictionary contains keys 'user_creation' and 'UID'.
    """
    users = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM user_register")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            user = {}
            user["UID"]  = i["UID"]
            user["user_creation_tstamp"]  = i["user_creation_tstamp"]
            users.append(user)
    except:
        users = []
    return users

def get_time_registry():
    """
    Retrieves all records from the 'time_registry' table and converts them into dictionaries.

    Returns:
        list: A list of dictionaries representing time registry records.
              Each dictionary contains keys 'user_registry_tstamp', 'UID', and 'id'.
    """
    time_registrys = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM time_registry")
        rows = cur.fetchall()
        
        # convert row objects to dictionary
        for i in rows:
            time_registry = {}
            time_registry["user_registry_tstamp"]  = i["user_registry_tstamp"]
            time_registry["UID"]  = i["UID"]
            time_registry["id"]  = i["id"]
            time_registrys.append(time_registry)
    except:
        time_registrys = []
    return time_registrys

def get_user_register_by_uid(uid):
    """
    Retrieves a user record from the 'user_register' table based on the provided UID.

    Parameters:
        uid (str): The UID (Unique ID) of the user to retrieve.

    Returns:
        dict: A dictionary representing the user record if found, otherwise an empty dictionary.
              The dictionary contains keys 'UID' and 'user_creation_tstamp' with corresponding values.
    """
    user = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM user_register WHERE UID = ?", (uid,))
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            user["UID"]  = i["UID"]
            user["user_creation_tstamp"]  = i["user_creation_tstamp"]
            
    except:
        user = {}
    return user

def get_time_registry_by_uid(uid):
    """
    Retrieves time registry records associated with a specific UID from the 'time_registry' table.

    Parameters:
        uid (str): The UID (Unique ID) used to filter time registry records.

    Returns:
        list: A list of dictionaries representing time registry records for the specified UID.
              Each dictionary contains keys 'UID', 'user_registry_tstamp', and 'id' with corresponding values.
              An empty list is returned if no records are found or an error occurs.
    """
    time_registrys = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM time_registry WHERE UID = ?", (uid,))
        rows = cur.fetchall()
        
        # convert row objects to dictionary
        for i in rows:
            time_registry = {}
            time_registry["UID"]  = i["UID"]
            time_registry["user_registry_tstamp"]  = i["user_registry_tstamp"]
            time_registry["id"]  = i["id"]
            time_registrys.append(time_registry)
    except:
        time_registrys = []
    return time_registrys

def add_user_ubidots(uid):
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
    request = requests.post(
        URL_UBIDOTS,
        headers={'X-Auth-Token': TOKEN_UBIDOTS, 'Content-Type': 'application/json'},
        json=data
    )
    return request.status_code
    
def add_time_registry_ubidots(uid, is_registered):
    """
    Sends an HTTP POST request to Ubidots API to add a time registry.

    Parameters:
        uid (str): The UID (User ID) associated with the time registry.
        is_registered (bool): True if the user is registered.

    Returns:
        int: HTTP status code of the request.
    """
    value = 1 if is_registered else 0
    data = {
        'add_time_registry': {
            'value': value,
            'context': {
                'UID': uid
            }
        }
    }
    request = requests.post(
        URL_UBIDOTS,
        headers={'X-Auth-Token': TOKEN_UBIDOTS, 'Content-Type': 'application/json'},
        json=data
    )
    return request.status_code

if __name__ == "__main__":

    app = Flask(__name__)
    
    @app.route('/api/insert_random_data', methods=['GET'])
    def api_initdb():
        return jsonify(insert_random_data())
    
    @app.route('/api/user_register', methods=['GET'])
    def api_get_user_register():
        return jsonify(get_user_register())
    
    @app.route('/api/user_register/<uid>', methods=['GET'])
    def api_get_user_register_by_id(uid):
        return jsonify(get_user_register_by_uid(uid))
    
    @app.route('/api/user_register/add', methods=['POST'])
    def api_add_user_register():
        user = request.get_json()
        return jsonify(insert_user_register(user))
    
    @app.route('/api/time_registry', methods=['GET'])
    def api_get_time_registry():
        return jsonify(get_time_registry())
    
    @app.route('/api/time_registry/<uid>', methods=['GET'])
    def api_get_time_registry_by_id(uid):
        return jsonify(get_time_registry_by_uid(uid))
    
    @app.route('/api/time_registry/add', methods=['POST'])
    def api_add_time_registry():
        time_registry = request.get_json()
        return jsonify(insert_time_registry(time_registry))

    app.debug = True
    app.run(host="0.0.0.0")
