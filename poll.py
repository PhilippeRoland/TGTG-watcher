import schedule
import time
import winsound
from utils import format_item
from datetime import datetime

frequency = 1000  # Set Frequency To 2500 Hertz
duration = 500  # Set Duration To 1000 ms == 1 second
last_item_ids=[]

def poll(client, debug):
    global last_item_ids
    print("Polling favorites " + str(datetime.now()))
    found_item=False
    allitems=client.get_items()
    for item in allitems:
        if(item['items_available'] > 0):
            if(item['item']['item_id'] not in last_item_ids) :
                found_item = True
            print("\t" + format_item(item) + (" - NEW" if found_item else ""))
    if(found_item):
        winsound.Beep(frequency, duration)
    last_item_ids=[item['item']['item_id'] for item in allitems]
    print("\n")

def start_poll(client, debug):
    print("Starting poll schedule...")
    schedule.every(1).minutes.do(poll, client, debug)
    poll(client, debug)
    while True:
        schedule.run_pending()
        time.sleep(1)