import requests
import time
from datetime import date, timedelta
import datetime
import pandas as pd
import calendar
from functions.utils import clean_dict_list, id_generator

########## SM TABLES ###########
def get_data(table, headers):

    # Send a GET request to the API endpoint with the headers
    URL = f"https://api.zelty.fr/2.7//catalog/{table}?show_all=1"
    status = 0
    retry_count = 0

    while status != 200 and retry_count < 2:
        r = requests.get(URL, headers=headers)
        status = r.status_code

        # If the status code is not 200, retry the request up to 2 times
        if status != 200:
            retry_count += 1
            time.sleep(3)
            print(f"{table} : status {status}, retrying in 3secs... retry count {retry_count}/2")
            print()

        else:      
            # Check if the API response contains data
            if not r.json().get(table):
                # If no data is present, indicate this in the output
                print(f"API response contains no {table} data")
                  
            else:
                # If data is present, extract it from the API response
                result = r.json()[table]
                page_results = len(result)
                print(f"{table}: status {status} -> successful data collection with {page_results} entries ")
                time.sleep(2)
                return result

########## MENUS ###########
def get_menus():

    table = "menus"

    # Define the API endpoint URL
    URL = f"https://api.zelty.fr/2.7/catalog/{table}?show_all=1&all_restaurants=1"

    # Send a GET request to the API endpoint with the headers
    status = 0
    retry_count = 0
    menus_raw = None

    print(f"Get {table} data...")

    while status != 200 and retry_count < 2:
        r = requests.get(URL, headers=headers)
        status = r.status_code

        # If the status code is not 200, retry the request up to 2 times
        if status != 200:
            retry_count += 1
            time.sleep(3)
            print(f"{table} : status {status}, retrying in 3secs... retry count {retry_count}/2")
            print()

        else:      
            # Check if the API response contains data
            if not r.json().get(table):
                # If no data is present, indicate this in the output
                print(f"API response contains no {table} data")
                
            else:
                # If data is present, extract it from the API response
                menus_raw = r.json()[table]
                page_results = len(menus_raw)
                print(f"{table}: status {status} -> successful data collection with {page_results} entries ")
                
    # Check if the variable menus_raw is not empty
    if not menus_raw:
        print(f"Could not get API response for {table} data")
        
    else:
        # Initialize empty lists
        menus = []
        menu_enable_hours = []
        menu_parts = []
        menu_parts_dishes_prices = []

        base_id = 3000
        menu_parts_add_id = 0
        menu_hours_add_id = 0
        menu_parts_dishes_add_id = 0

        useless_menus_keys = [
            'parts',
            'enable_hours',
            'tags',
            'meta'
        ]

        # Loop through each menu in the `menus_raw` list
        for menu in menus_raw:
            # Extract the relevant data from the current menu, and append it to the `menus` list as a dictionary
            menus.append({
                **{key: menu[key] for key in menu.keys() if key not in useless_menus_keys},
            })

            # Sometimes hours are missing
            if menu.get('enable_hours'):
                # Get the 2 hour period of each day
                for day, times in menu['enable_hours'].items():
                    # Sometimes hour periods are missing
                    
                    if times:
                        # Generate ids
                        #menu_hours_id = base_id + menu_hours_add_id
                        #menu_hours_add_id += 1

                        menu_enable_hours.append({
                            #'id': menu_hours_id,
                            'menu_id': menu['id'],
                            'day': day,
                            'enable_hour_from': times[0][0] if times[0] else None,
                            'enable_hour_to': times[0][1] if times[0] else None
                        })
                   

            # Loop through each part in the `parts` list of the current menu
            
            
            for menu_part in menu['parts']:
                # Generate ids
               # menu_parts_id = base_id*2 + menu_parts_add_id
               # menu_parts_add_id += 1
                # Extract the relevant data from the current part and menu,
                # and append it to the `menu_parts` list as a dictionary
                menu_parts.append({
                    #'id': menu_parts_id,
                    'part_id': menu_part['id'],
                    'menu_id': menu['id'],
                    **{key: menu_part[key] for key in menu_part.keys() if key not in ['id', 'dishes_prices', 'dishes']}
                })
                

                # Loop through each dish in the `dishes` list of the current menu part
                for dish in menu_part['dishes']:
                    # Generate ids
                    #menu_parts_dishes_id = base_id*3 + menu_parts_dishes_add_id
                    #menu_parts_dishes_add_id += 1
                    # Extract the relevant data from the current menu part and dish,
                    # and append it to the `menu_parts_dishes_prices` list as a dictionary
                    menu_parts_dishes_prices.append({
                        #'id': menu_parts_dishes_id,
                        'dishes_id': dish,
                        'part_id': menu_part['id'],
                        'menu_id': menu['id'],
                        'price': menu_part['dishes_prices'].get(str(dish))
                    })

        menu_enable_hours = id_generator(list_dict=menu_enable_hours, base_id=4000)
                
        # Return the `menu_parts_dishes_prices` list
        return {
            "menus": menus,
            "menu_enable_hours": menu_enable_hours,
            "menu_parts": menu_parts,
            "menu_parts_dishes_prices": menu_parts_dishes_prices
        }

########## OPTIONS ###########
def get_options(headers):

    table = "options"

    # Set the URL to the API endpoint
    URL = f"https://api.zelty.fr/2.7//catalog/{table}?show_all=1?all_restaurants=1"

    ## Send a GET request to the API endpoint with the headers
    status = 0
    retry_count = 0
    options_raw = None

    print(f"Get {table} data...")

    while status != 200 and retry_count < 2:
        r = requests.get(URL, headers=headers)
        status = r.status_code

        # If the status code is not 200, retry the request up to 2 times
        if status != 200:
            retry_count += 1
            time.sleep(3)
            print(f"{table} : status {status}, retrying in 3secs... retry count {retry_count}/2")
            print()

        else:      
            # Check if the API response contains data
            if not r.json().get(table):
                # If no data is present, indicate this in the output
                print(f"API response contains no options data")
                
            else:
                # If data is present, extract it from the API response
                options_raw = r.json()[table]
                page_results = len(options_raw)
                print(f"{table}: status {status} -> Successful data collection with {page_results} entries ")

    if not options_raw:
        print(f"Could not get API response for {table} data")

    else:
        # Initialize an empty list to store the extracted options and option values data data
        options = []
        option_values = []

        # Loop through each option in the `options_raw` list
        for option in options_raw:
            
            # Extract the relevant option data, excluding the `values` key, and append it to the `options` list as a dictionary
            options.append({key: option[key] for key in option.keys() if key not in ['values']})

            # Loop through each value in the `values` list of the current option
            for value in option['values']:
                
                # Extract the relevant data from the current option value,
                # and append it to the `option_values` list as a dictionary
                option_values.append({
                    'id': value['id'],
                    'option_id': option['id'],
                    **{key: value[key] for key in value.keys() if key not in ['id']}
                })

        # Return the `options` and `option_values` lists with the extracted data
        return {
            "options": options,
            "option_values": option_values
        }

########## RESTAURANTS ###########
def get_restaurants(headers):

    table = "restaurants"

    # Define the API endpoint URL
    URL = f"https://api.zelty.fr/2.7/{table}"

    # Send a GET request to the API endpoint with the headers
    status = 0
    retry_count = 0
    restaurants_raw = None

    print(f"Get {table} data...")

    while status != 200 and retry_count < 2:
        r = requests.get(URL, headers=headers)
        status = r.status_code

        # If the status code is not 200, retry the request up to 2 times
        if status != 200:
            retry_count += 1
            time.sleep(3)
            print(f"{table} : status {status}, retrying in 3secs... retry count {retry_count}/2")
            print()

        else:      
            # Check if the API response contains data
            if not r.json().get(table):
                # If no data is present, indicate this in the output
                print(f"API response contains no {table} data")
                
            else:
                # If data is present, extract it from the API response
                restaurants_raw = r.json()[table]
                page_results = len(restaurants_raw)
                print(f"{table}: status {status} -> successful data collection with {page_results} entries ")
                
    # Check if the variable menus_raw is not empty
    if not restaurants_raw:
        print(f"Could not get API response for {table} data")
        
    else:

        restaurants = []
        restaurant_delivery_hours = []
        restaurant_opening_hours = []

        list_tables = [
            restaurant_delivery_hours,
            restaurant_opening_hours
        ]

        for restaurant in restaurants_raw:

            restaurants.append({

                # Drop dict keys and get keys from the dict
                **{key: restaurant[key] for key in restaurant.keys() if key not in ['loc', 'opening_hours', 'delivery_hours']},
                'lat': restaurant['loc']['lat'],
                'lng': restaurant['loc']['lng']

            })

        hour_tables = ['delivery', 'opening']

        # process delivery hours then opening hours
        for table, list_table in zip(hour_tables, list_tables):

            # for each restaurant, we get the delivery/opening hours
            for restaurant in restaurants_raw:

                # Sometimes hours are missing
                if restaurant[f'{table}_hours'] is not None:

                    # Get the 2 hour period of each day
                    for day, times in restaurant[f'{table}_hours'].items():

                        # Sometimes hour periods are missing
                        if times:
                            list_table.append({

                                'restaurant_id': restaurant['id'],
                                'day': day,
                                f'{table}_hour_from': times[0][0] if times[0] else None,
                                f'{table}_hour_to': times[0][1] if times[0] else None,
                                f'{table}_hour_from_2': times[1][0] if len(times) > 1 and times[1] else None,
                                f'{table}_hour_to_2': times[1][1] if len(times) > 1 and times[1] else None

                                })

                        # Insert None if no values at all
                        else:
                            list_table.append({

                                'restaurant_id': restaurant['id'],
                                'day': day,
                                f'{table}_hour_from': None,
                                f'{table}_hour_to': None,
                                f'{table}_hour_from_2': None,
                                f'{table}_hour_to_2': None

                            })

        restaurant_delivery_hours = id_generator(list_dict=list_tables[0], base_id=3000)
        restaurant_opening_hours = id_generator(list_dict=list_tables[0], base_id=2000)

        return {
            "restaurants": restaurants,
            "restaurant_delivery_hours": restaurant_delivery_hours,
            "restaurant_opening_hours": restaurant_opening_hours
        }

########## CUSTOMERS ###########
def get_customers(since, headers):

    table = "customers"

    if since:
        date_obj = datetime.datetime.strptime(since, '%Y-%m-%dT%H:%M:%S%z')
        last_date = date_obj.isoformat()
        from_date = date_obj.strftime("%Y-%m-%d")

    else:
        from_date = "2023-02-15"
        last_date = from_date

    # Define variables for pagination and JSON data storage
    jsons=[]
    call = 0
    limit = 1000
    offset = 0
    querystring = {"limit":limit}
    has_more = True
    day_count = 0
    updates = []
  
    # Continue making API calls until no more results are returned
    while has_more is True:

        status = 0
        retry_count = 0

        if updates:
            last_update = max(updates)
            from_date = datetime.datetime.strptime(last_update, '%Y-%m-%dT%H:%M:%S%z')
            from_date = from_date.strftime("%Y-%m-%d")

        while status != 200 and retry_count < 2:
            r = requests.get(
                f"https://api.zelty.fr/2.7/{table}?offset={offset}&updated_after={from_date}", 
                headers=headers, 
                params=querystring
                )

            status = r.status_code

            # If the status code is not 200, retry the request up to 2 times
            if status != 200:
                retry_count += 1
                time.sleep(3)
                print(f"{table} : status {status}, retrying in 3secs... retry count {retry_count}/2")
                print()

            else:
                if r.json().get(table):
                    # If customers are returned, append them to the JSON data storage and increment the offset and call count
                    result = r.json()[table]
                    jsons.append(result)
                    call += 1
                    day_count += 1
                    page_results = len(result)
                    time.sleep(2) # Wait for 2 second before making the next API call
                    for customer in result:
                        updates.append(customer['updated_at'])
                    print(f"{table} call n° {call}: status {status} -> Successful data collection with {page_results} entries from {from_date}")

                    if len(result) < limit: # Stop the loop when no more results are returned
                        has_more = False
                        print(f"Break loop : total results from {from_date} < {limit}")
                    
                else:
                    # If no data is present, indicate this in the output
                    time.sleep(2)
                    has_more = False # Stop the loop when no more results are returned
                    print(f"Break loop : 0 result from {from_date}")
                    
    # Check if jsons is empty
    if not jsons:
        print(f"Could not get API response for {table} data")

    else:
        # If not empty, clean the dictionary list and store it in customers
        customers = clean_dict_list(jsons)
        # Create a list of update dates for each customer
        update_dates = [i['updated_at'] for i in customers]
        # Find the most recent update date and store it in last_update
        last_update = max(update_dates)

        return {
            "customers": customers,
            "last_update": last_update
            }

########## CLOSURES ###########
def get_closures(since, headers):

    table = "closures"

    # Check if "since" argument is passed
    if since:
        # Try to parse the date string to a datetime object
        try:
            date_obj = datetime.datetime.strptime(since, '%Y-%m-%dT%H:%M:%S%z')
        # If there is a ValueError, print the error message and set the "from_date" variable to "since"
        except ValueError as v:
            print(v, "-> keep current date format as the from date")
            from_date = since
        # If the date string is successfully parsed, convert it back to a string in isoformat and set "from_date" to a date string format
        else:
            last_date = date_obj.isoformat()
            from_date = date_obj.strftime("%Y-%m-%d")
            
    # Use this date if no "since" argument is passed        
    else:
        from_date = "2023-02-15"
        last_date = from_date

    # Define variables for pagination and JSON data storage
    jsons=[]
    call = 0
    limit = 200
    offset = 0
    has_more = True
    day_count = 0
    create_dates = []
  
    # Continue making API calls until no more results are returned
    while has_more is True:

        status = 0
        retry_count = 0

        while status != 200 and retry_count < 2:

            r = requests.get(
                f"https://api.zelty.fr/2.7/{table}", 
                headers=headers, 
                params= {"limit":limit, "offset": offset, "after": from_date}
                )

            status = r.status_code

            # If the status code is not 200, retry the request up to 2 times
            if status != 200:
                retry_count += 1
                time.sleep(3)
                print(f"{table} : status {status}, retrying in 3secs... retry count {retry_count}/2")
                print()

            else:
                if r.json().get(table):
                    # If customers are returned, append them to the JSON data storage and increment the offset and call count
                    result = r.json()[table]
                    jsons.append(result)
                    offset += limit
                    call += 1
                    day_count += 1
                    page_results = len(result)
                    time.sleep(2) # Wait for 2 second before making the next API call

                    print(f"{table} call n° {call}: status {status} -> Successful data collection with {page_results} entries from {from_date}")

                    if page_results < limit: # Stop the loop when no more results are returned
                        has_more = False
                        print(f"Break loop : total results from {from_date} < {limit}")
                    
                else:
                    # If no data is present, indicate this in the output
                    time.sleep(2)
                    has_more = False # Stop the loop when no more results are returned
                    print(f"Break loop : 0 result from {from_date}")
                    
    # Check if jsons is empty
    if not jsons:
        print(f"Could not get API response for {table} data")
        closures = None
        last_closure = from_date

    else:
        # If not empty, clean the dictionary list and store it in customers
        closures = clean_dict_list(jsons)
        # Create a list of update dates for each customer
        create_dates = [i['created_at'] for i in closures]
        # Find the most recent update date and store it in last_update
        last_closure = max(create_dates)

    return {
        "closures": closures,
        "last_closure": last_closure
        }

########## ORDERS ###########

def get_orders(since):
    table = "orders"

    if since:
        date_obj = datetime.datetime.strptime(since, '%Y-%m-%dT%H:%M:%S%z')
        last_date = date_obj.isoformat()
        from_date = date_obj.strftime("%Y-%m-%d")

    else:
        from_date = "2023-02-15"
        last_date = from_date

    # Create a list of dates from input date to (today - 1 day), in yyyy-mm-dd format
    first_days = pd.date_range(from_date, end=datetime.datetime.today() - timedelta(days=1), freq='D').strftime('%Y-%m-%d').tolist()

    # Convert each date from string to datetime object
    first_days = [datetime.datetime.strptime(i, '%Y-%m-%d').date() for i in first_days]

    # Initialize empty list to store API responses, and counters for API calls and number of days
    jsons = []
    days_count = 0
    call = 0
    total_results = 0

    # For each day in the list of dates
    for day in first_days:
        # Initialize variables for pagination and API call count
        limit = 100
        page_results = 0
        has_more = True
        last_day_collected = None
        offset = 0

        # While loop runs as long as the API has not been called 3 times or all orders for the day have been processed
        while has_more is True:
            # Define query string parameters for API request
            querystring = {"limit": limit, "offset": offset}

            # Make API request and handle exceptions
            status = 0
            retry_count = 0
            while status != 200 and retry_count < 2:

                try:
                    r = requests.get(f"https://api.zelty.fr/2.7/{table}?from={day}&to={day}" \
                        "&expand[]=customer"\
                        "&expand[]=items" \
                        "&expand[]=transactions" \
                        "&expand[]=transactions.method" \
                        "&expand[]=price" \
                        "&expand[]=price.discounts", headers=headers, params=querystring)

                    status = r.status_code
                    if status != 200:
                        retry_count += 1
                        time.sleep(3)
                        print(f"status {status}, retrying in 3secs... retry count {retry_count}/3")
                        print()

                except ConnectionError as c:
                    print(c)
                else:

                    # Check if API response contains any orders
                    if r.json().get(table):
                        offset += 100
                        # Append API response to jsons list
                        jsons.append(r.json()[table])
                        call += 1
                        last_day_collected = day
                        page_results = len(r.json()[table])
                        total_results += page_results
                        time.sleep(2)  # Wait 2 seconds before making next API call
                        # Print API response details
                        print(f"API call n° {call}, status {status}: {page_results} {table} on {day} ")
                        # Break while loop if API response has fewer than 100 orders
                        if page_results < limit:
                            print("Break loop : results on this day < 100")
                            days_count += 1
                            has_more = False
                            break

                    # Break while loop if response contains no orders
                    else:
                        page_results = 0
                        has_more = False
                        last_day_collected = day
                        time.sleep(2)
                        print(f"Break loop : 0 result on {day}")

        # Number of days processed
        print("Days processed: ", days_count) 
        print()

        # If API has been called more than 8 times and all orders for the day have been processed, break out of the loop
        if call > 20 and has_more is False:
            print("Stop loop")
            print(f"{table}: successful data collection with {total_results} entries from {days_count} days processed")
            break

    has_more = True

    if last_day_collected == first_days[-1]:
        has_more = False
        print(f"Has more = {has_more} : No more result, end of collection")
    else:
        print(f"Has more = {has_more} : Function will re-run")

    # Check if the variable jsons is not empty
    if not jsons:
        print("Could not get API response for options data")

    else:
        # Call the function clean_dict_list() passing the jsons variable as argument
        # Assign the result of this function to the variable orders_raw
        orders_raw = clean_dict_list(jsons)

        # Create empty lists for the different categories of orders
        orders = []
        order_dates = []
        order_prices = []
        order_price_discounts = []
        order_transactions = []
        order_items = []
        order_items_prices = []
        order_items_modifiers = []
        order_items_modifiers_prices = []

        useless_order_keys = [
        'price',
        'items',
        'transactions',
        'customer'
        ]

        items_keys = [
            'name',
            'type',
            'item_id',
            'price',
            'modifiers'
        ]

        order_transactions_keys = [
            "device_id",
            "price",
            "date",
            "method"
        ]

        # Loop through each order in the list of orders
        for order in orders_raw:
            #if from_date < order['created_at']:

            #print("Since:", last_date, "/ created_at: ",order['created_at'])
            orders.append({
                **{key: order[key] for key in order.keys() if key not in useless_order_keys},
                'customer_id': order['customer']['id'] if order.get('customer') else None
            })
            # Get list of all create dates
            order_dates.append(order['created_at'])


            ### Extracting order prices ###
            
            # Create a dictionary to hold the order price information and append it to the list of order prices
            order_prices.append({
                'order_id': order['id'],
                **{key: order['price'][key] for key in order['price'].keys() if key not in ['discounts']}
            })

            ### Extracting order price discounts ###

            # If there are discounts in the order's price
            if order['price']['discounts'] is not None:
                # For each discount in the order's price, create a dictionary to hold the discount information and append it to the list of order price discounts
                for discount in order['price']['discounts']:
                    order_price_discounts.append({
                        'order_id': order['id'],
                        'type': discount['type'] if discount['type'] else None,
                        'amount': discount['amount'] if discount['amount'] else None,
                        'label': discount['label'] if discount['label'] else None
                    })

            ### Extracting order transacitons ###

            # If the transactions exist for the order
            if order['transactions'] is not None:
                # For each transaction in the order
                for transaction in order['transactions']:
                    # Create a dictionary to hold the transaction information
                    row = {
                        'order_id': order['id']
                    }
                    
                    # Add other keys to the dictionary
                    for key in order_transactions_keys:
                        row[key] = transaction.get(key, None)
                    
                    # Add the new dictionary to the list of order transactions
                    order_transactions.append(row)

            # If the items exist
            if order['items'] is not None:
                
                ### Extracting order items ###
                
                # For each item in the order
                for item in order['items']:
                    # create a dictionary to hold the item information
                    row = {
                        'item_id': item.get('item_id', None),
                        'order_id': order['id']
                    }
                    
                    # add other keys to the dictionary
                    for key in [k for k in items_keys if k not in ['item_id', 'price', 'modifiers']]:
                        row[key] =  item.get(key, None)
                    
                    # add the new dictionary to the list of order items
                    order_items.append(row)

                    ### Extracting order items price ###
                    
                    # create a dictionary to hold the item price information
                    order_items_prices.append({
                        'item_id': item['item_id'],
                        'order_id': order['id'],
                        **{key: item['price'][key] for key in item['price'].keys() if key not in ['tax']}
                    })

                    ### Extracting order item modifiers ###
                    
                    # If the item has modifiers
                    if item['modifiers'] is not None:
                        # For each modifier of the item
                        for modifier in item['modifiers']:
                            # create a dictionary to hold the modifier information
                            order_items_modifiers.append({
                                'item_id': item['item_id'],
                                'order_id': order['id'],
                                **{key: modifier[key] for key in modifier.keys() if key not in ['price', 'modifiers']},
                            })

                            ### Extracting order item modifier price ###
                            
                            # If the modifier has a tax
                            if 'tax' in modifier['price']:
                                # create a dictionary to hold the modifier price information
                                order_items_modifiers_prices.append({
                                    'modifier_id': modifier['id'],
                                    'item_id': item['item_id'],
                                    'order_id': order['id'],
                                    **{key: modifier['price'][key] for key in modifier['price'].keys() if key not in ['tax']},
                                    'tax_amount': modifier['price']['tax']['tax_amount'],
                                    'tax_rate': modifier['price']['tax']['tax_rate']
                                })
                            
                            # If the modifier does not have a tax
                            else:
                                # create a dictionary to hold the modifier price information
                                order_items_modifiers_prices.append({
                                    'modifier_id': modifier['id'],
                                    'item_id': item['item_id'],
                                    'order_id': order['id'],
                                    **{key: modifier['price'][key] for key in modifier['price'].keys() if key not in ['tax']},
                                    'tax_amount': None,
                                    'tax_rate': None
                                })

        return {
            'orders': orders,
            'order_prices': order_prices,
            'order_price_discounts': order_price_discounts,
            'order_transactions': order_transactions,
            'order_items': order_items,
            'order_items_prices': order_items_prices,
            'order_items_modifiers': order_items_modifiers,
            'order_items_modifiers_prices': order_items_modifiers_prices,
            'last_order': max(order_dates),
            'has_more': has_more
                }

