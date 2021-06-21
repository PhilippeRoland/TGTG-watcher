from tgtg import TgtgClient
import json
import schedule
import time
import winsound
from utils import format_item
from datetime import datetime

frequency = 1000  # Set Frequency To 2500 Hertz
duration = 500  # Set Duration To 1000 ms == 1 second

def poll(client, debug):
    print("Polling favorites " + str(datetime.now()))
    found_item=False
    for item in client.get_items():
        if(item['items_available'] > 0):
            print("\t" + format_item(item))
            found_item = True
    if(found_item):
        winsound.Beep(frequency, duration)
    print("\n")

def start_poll(client, debug):
    print("Starting poll schedule...")
    schedule.every(1).minutes.do(poll, client, debug)
    #TODO only poll for new items
    poll(client, debug)
    while True:
        schedule.run_pending()
        time.sleep(1)