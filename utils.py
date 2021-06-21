import json

def dump_item(item):
    print(json.dumps(item, indent=4, sort_keys=True))

def format_item(parent_item):
    item = parent_item['item']
    store = parent_item['store']
    
    txt = "{} - {} : {:.2f} {} Available amount:{}"
    return (txt.format(
        store['store_name'], 
        item['item_category'], 
        float(item['price_including_taxes']['minor_units'])*(0.1**item['price_including_taxes']['decimals']),
        item['price_including_taxes']['code'],
        parent_item['items_available']))

def print_api_error(api_error):
    print ("Encountered an error while calling TGTG API. {} - {}".format(api_error.args[0], api_error.args[1]))
    
def log(string, debug_mode):
    if debug_mode: 
        print('DEBUG - '+string)
