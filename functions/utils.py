#### useful functions ###

def clean_dict_list(dict_list):

    # Initialize an empty list to store the cleaned dictionary
    clean_dictionary = []

    # Loop through each dictionary in the input `dict_list`
    for dictionary in dict_list:
        
        # Loop through each key-value pair in the current dictionary,
        # and append it to the `clean_dictionary` list as a new dictionary
        for j in dictionary:
            clean_dictionary.append(j)
    
    # Return the cleaned dictionary
    return clean_dictionary

def id_generator(list_dict, base_id):
    # Loop through the list of dictionaries and add an 'id' key to each dictionary with a unique id
    for i in range(len(list_dict)):
        list_dict[i]['id'] = i+base_id

    data = []
    # Loop through the list of dictionaries again and create a new list of dictionaries without the 'id' key
    for item in list_dict:
        data.append({
            'id': item['id'],
            **{key: item[key] for key in item.keys() if key != 'id'}
        })

    # Return the new list of dictionaries
    return data
