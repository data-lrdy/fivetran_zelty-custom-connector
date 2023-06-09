# Zelty API Data Retrieval
This repository contains Python code that uses the requests library to retrieve data from the Zelty API endpoint. The API returns JSON data which is then used to extract relevant information and create structured data.

## Installation
To use the code, first clone this repository:

```bash
git clone https://github.com/data-lrdy/fivetran_zelty-custom-connector.git
```

Then, install the necessary dependencies:

```bash
pip install requests
```
## Usage
The main code of this repository can be found in the api_requests.py file. This file contains the function get_data(table, headers), which retrieves data for a given table from the Zelty API. The function takes two parameters:

table: a string that specifies the name of the table to retrieve data from.
headers: a dictionary that contains the necessary authorization headers to access the API endpoint.
The get_data function uses a GET request to retrieve data from the API endpoint, and returns the data in JSON format.

There is also other bigger functions called 
- get_menus
- get_orders
- get_closures
- get_customers
- get_options
- get_restaurants

which are used to retrieve data with pagination system. The function only accepts the "headers" parameter and retrieves data from the entities that have already been specified within the function. Certain entities may require an additional parameter "since", which indicates the last row retrieved from the preceding API call.

## Example
Here's an example of how to use the get_data function to retrieve data from the "users" table:

```python
import requests
from functions.api_requests import get_data, get_orders

headers = {"Authorization": "Bearer <YOUR_ACCESS_TOKEN>"}

# Tags
tags = get_data(table="tags", headers=headers)
# Orders
orders_json = get_orders(since='2023-02-01', headers=headers)
orders = orders_json['orders']
``` 

This will retrieve data for all tags and orders from '2023-02-01', and return the data in JSON format.

## Credits
This code was written by Louis Raverdy.
