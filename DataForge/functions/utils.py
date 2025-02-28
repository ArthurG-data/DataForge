
from typing import Sequence, Optional
from  argparse import ArgumentParser,RawDescriptionHelpFormatter
from classes.classmodules import Args
from tqdm.asyncio import tqdm
from dotenv import load_dotenv, set_key
from psycopg2.extras import execute_values
from database_manager.scripts.postreg_get_database import initialise_db_connection

import aiohttp, datetime, asyncio,  os, requests, time,  textwrap, psycopg2

'''
--------------------------------------------------------------------------------------------------------------------------------------
functions related to the main
--------------------------------------------------------------------------------------------------------------------------------------
'''

def sigterm_handler(_, __):
    raise SystemExit(1)

def parse_args(argv:Optional[Sequence[str]]=None) -> Args:
    parser = ArgumentParser(prog="MTGstock Parser",
                                     formatter_class=RawDescriptionHelpFormatter,
                                     description=textwrap.dedent('''\
                                        Table ID Creator - An Amazing Parser!
                                        -------------------------------------
                                        Interacts with the card_id database for the ebay_app.''')
                                     )
    parser.add_argument("-l", "--last",  action="store_true", help="The last MTGstock id present in the table")
    parser.add_argument("-c","--count", action="store_true", help="The number of card entry in the card_id table")
    parser.add_argument("-u","--update",  action="store_true", help="Update the table with new entries, if the last valid online is different from the last in the table")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", help="Prints more messages, useful for debugging", action="store_true")
    group.add_argument("-q", "--quiet", help="Remove the display of messages", action="store_true")
    parser.add_argument("x",nargs="?",type=int, default=100,help="The size of each batch for the api calls to mtgdtoacks")
    return Args(**parser.parse_args(argv).__dict__)

'''
--------------------------------------------------------------------------------------------------------------------------------------
accessory functions
--------------------------------------------------------------------------------------------------------------------------------------
'''


def create_new_table(query):
    """
    function: execute a query
    inputs: parameters for connection and query to execute
    outputs: na
    """
    conn, cursor = initialise_db_connection()
    conn.rollback()
    try:
        cursor.execute(query)
        conn.commit()
        print("Query Executed")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback() 
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        
def insert_new_cards(cards_list):
    """
    function: creates a quesry to add a card to the card table
    inputs: List of tuples (mtg_stock_id, scry_id, TCG_id, card_name)

    """
    query = """
    INSERT INTO card_id (mtg_stock_id, scry_id, TCG_id, card_name)
    VALUES %s
    ON CONFLICT (scry_id) DO NOTHING;
    """
    print(f"Query to insert {len(cards_list)} new cards")
    try:
        conn, cursor = initialise_db_connection()
        execute_values(cursor, query, cards_list)
        conn.commit()
        print(f"Added {len(cards_list)} cards to the table")
    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback()
        print(error)
        
    
'''
--------------------------------------------------------------------------------------------------------------------------------------
functions related making api calls
--------------------------------------------------------------------------------------------------------------------------------------
'''
# load env variable
load_dotenv()
SEMAPHORE = asyncio.Semaphore(2)
SLEEP_TIME = 240
#functions to import the data
api_endpoint_finance = os.getenv(
    "API_MTGSTOCK_ENDPOINT")

headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Encoding": "gzip, deflate, br",
"Connection": "keep-alive",
}

def get_header():
    return headers

def extract_params_prints_mtgstocks(json_file, params=["id", "scryfallId", "tcg_id", "name"]):
    """
    function: make a call to the api of mtg stocks to get the information to create the card table
    inputs: the card is from mtgstocks and the required infos
    outputs: a dict with the params as key and info as values
    """
    response_list = []
    for param in params:
        value = json_file.get(param)
        if value:
            response_list.append(value)
        else:
            return
    return tuple(response_list)


def get_mtgstock_api_cards():
    return api_endpoint_finance

def make_request(url):
    """
    role: Check if the url is accessible
    input: the complete url and the header to simulate a request
    output: the response if successful, else None
    """
    try:
        response = requests.get(url,headers=get_header())
        
        if response.status_code == 200:
            print("Request Successful")
            return response.json()
        else:
            print(f"Request Failed with status code: {response.status_code}")
            return None
        
    except Exception as e:
        print(f"Error while making the request: {str(e)}")
        return None
        
def get_prices_id(unique_id):
    """
    role: get the prices in a json files from a unique card ID
    input: the unique card id and the headers
    output: a dict with 
    """
    request_url = f"{api_endpoint_finance}/prints/{unique_id}/prices"
    response = make_request(request_url, get_header())
    if response:
        return response
    else:
        print("Error while fetching prices from card ID")
        
def get_dict_entry(dictionnary, entry):
    """
    function: take a key from the value dict and return 2 list, one for x and y
    input: the dictionnation from the finance API and the key
    output: [x=unix epochs], [y=$AUD]
    """
    entry_points = dictionnary[f"{entry}"]
    x, y = zip(*entry_points)
    new_x = []
    for val in x:
        val = int(val /1000)
        if isinstance(val, (int)) and val <= int(time.time()):
            temp = datetime.fromtimestamp(val)
            new_x.append(temp)
    return new_x, y

def prices_json_to_dict_from_id(unique_id):
    """
    function: create a dict with the series from json file response from finance api endpoint
    input: the card id
    output: a dict with availble info as keys, time and value as entries
    """
    dict_prices = get_prices_id(unique_id)
    prices_dict = {}
    for key in dict_prices.keys():
        prices_dict[key] = get_dict_entry(dict_prices, key)
    return  prices_dict


async def check_connection_status(session, unique_id):
    request_url = f"{get_mtgstock_api_cards()}/prints/{unique_id}/"
    async with session.get(request_url, headers=get_header()) as response:
        return response.status == 200

async def find_last_entry(start_index, end_index=1000000):
    """
    find the hisghest number and return it
    """
    low = start_index
    high = end_index
    async with aiohttp.ClientSession() as session:
        while high > low:
            middle = (high+low) // 2
            print(middle)
            if await check_connection_status(session, middle):
                low = middle+1
            else:
                high = middle-1
    return low

def update_env(key, id):
    """
    change the higest  number
    """
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','..', '.env')) 
    set_key(dotenv_path, key, str(id))
    print(f"Saved {key}={id} at {dotenv_path}" )


async def fetch_card(session,unique_id, queue, max_retries=3):
    """
    function: fetched card info from mtgstocks, synchronuously. If max request reached, wait 1 min before making a new one. Will attempt a request at most max retries time
    inputs: a valid postgres session, the card mtg_stockId, the header and max number of retries
    output: a json file with the info for the seleted card
    """
    
    async with SEMAPHORE:  # Limit concurrent requests
        request_url = f"{get_mtgstock_api_cards()}/prints/{unique_id}/"
        for attempt in range(max_retries):
            try:
                async with session.get(request_url, headers=get_header()) as response:

                    if response.status == 200:
                        await queue.put(1) 
                        return await response.json()
                    elif response.status == 429:
                        print(f"429 Forbidden for {unique_id}, retrying in {SLEEP_TIME} seconds... (Attempt {attempt + 1}/{max_retries})")
                        await asyncio.sleep(SLEEP_TIME)
                        continue
                    else:
                        print(f"Request failed with status {response.status} for {unique_id}")
                        await queue.put(1) 
                        return None

            except aiohttp.ClientError as e:
                print(f"Network error fetching {unique_id}: {e}")
                return None
        print(f"Max retries reached for {unique_id}, skipping...")
        return None

async def progress_tracker(queue, total_cards):
    """Tracks and displays progress."""
    completed = 0
    with tqdm(total=total_cards, desc="Fetching Cards", unit="card") as progress:
        while completed < total_cards:
            await queue.get()
            progress.update(1)
            completed +=1
            queue.task_done()

async def batch_fetch_cards(id_start, id_end):
    """Fetches price data for multiple unique_ids concurrently."""
    total_cards = id_end - id_start
    queue = asyncio.Queue()

    async with aiohttp.ClientSession() as session:
     

      
        tasks = [fetch_card(session, uid, queue) for uid in range(id_start, id_end)]
        progress_task = asyncio.create_task(progress_tracker(queue, total_cards))
        result = await asyncio.gather(*tasks)# Run all requests concurrently
        await progress_task
    print("Batch fetch completed!")
    return result

def create_list_sql(cards):
    cards_extracted = []
    for card in cards:
        cards_extracted.append(extract_params_prints_mtgstocks())

async def fetch_all_cards(first_entry, last_entry, step=100):
    """Fetches cards in batches asynchronously."""
    while first_entry < last_entry:
        # Fetch batch
        cards = await batch_fetch_cards(first_entry, first_entry + step)
        print("Batch importation completed")
        
        # Extract valid cards
        cards_extracted = [extract_params_prints_mtgstocks(card) for card in cards if card]
        
    
        insert_new_cards(cards_extracted)
        
        # Update first_entry to move to next batch
        first_entry += step  
