#!/bin/sh

# Check if the database directory exists, if not, create it (Only for the first run)
if [ ! -d "database" ]; then
    mkdir database
fi

# Initialize the database
python3 initdb.py

# Start the API
python3 api.py
