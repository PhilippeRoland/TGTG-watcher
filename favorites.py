from tgtg import TgtgAPIError
from utils import print_api_error, format_item, log
from difflib import get_close_matches

def list_favorites(client):
    try :
        items = client.get_items(
            favorites_only=True,
            latitude=43.6043,
            longitude=1.4437,
            radius=10,
            page_size=400)
        #TODO debug
        for item in items:
            if(item['items_available'] > 0):
                print("\t" + format_item(item))
        print('\n')
    except TgtgAPIError as err:
        print_api_error(err)
        
def closest_favorite(client, new_favorite_name, debug):
    try :
        items = client.get_items(
            favorites_only=False,
            latitude=43.6043,
            longitude=1.4437,
            radius=10,
            page_size=400)
        log('Finding stores with closest names to \"{}\". {} items found in search range'.format(new_favorite_name, len(items)), debug)
        store_names = [ item['store']['store_name'] for item in items ]
        close_matches = get_close_matches(new_favorite_name, store_names, 10, 0.4)
        #TODO debug, recode algorithm
        closest_match = close_matches[0]
        for item in items:
            if(item['store']['store_name'] == closest_match):
                return closest_match, item['item']['item_id']
    except TgtgAPIError as err:
        print_api_error(err)
        
def add_favorite(client, new_favorite_id):
    try :
        client.set_favorite(item_id=new_favorite_id, is_favorite=True)
    except TgtgAPIError as err:
        print_api_error(err)
        
def rm_favorite(client, favorite_id):
    try :
        client.set_favorite(item_id=favorite_id, is_favorite=False)
    except TgtgAPIError as err:
        print_api_error(err)