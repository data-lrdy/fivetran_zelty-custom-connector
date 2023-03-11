import requests
import time
from datetime import date, timedelta
import datetime
import pandas as pd
import calendar
from functions.api_requests import get_data, get_menus
import json

# Open and read the JSON configuration file
with open('config.json') as f:
    config = json.load(f)

# Extract the API key from the configuration file and create a header with the key
KEY = config['key']
headers = {'Authorization': f"Bearer {KEY}"}

# Call the get_menus function with the headers
data = get_menus(headers)
print(data)
