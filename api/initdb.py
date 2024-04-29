import sqlite3
import os

if __name__ == '__main__':
    try:
        # Create the directory if it doesn't exist
        os.makedirs('database', exist_ok=True)
        print("Database directory created successfully.")

        # Create the database file if it doesn't exist
        open('database/database.db', 'a').close()
        print("Database file created successfully.")

        # Establish connection to the database
        conn = sqlite3.connect('database/database.db')
        print("Connection to the database established successfully.")

        # Create user_register table
        conn.execute('''
                    CREATE TABLE IF NOT EXISTS user_register (
                        UID    TEXT PRIMARY KEY NOT NULL,
                        user_creation_tstamp TEXT NOT NULL
                    )
        ''')
        print("Table 'user_register' created successfully.")

        # Create time_registry table
        conn.execute('''
                    CREATE TABLE IF NOT EXISTS time_registry (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_registry_tstamp TEXT NOT NULL,
                        UID TEXT NOT NULL REFERENCES user_register(UID)
                    )
         ''')

        print("Table 'time_registry' created successfully.")

        # Commit changes
        conn.commit()
        print("Changes committed successfully.")
    except Exception as e:
        print(e)
        print("Table creation failed")
    finally:
        conn.close()
