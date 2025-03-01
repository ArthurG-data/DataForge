
import os, asyncio
from dotenv import load_dotenv 
from DataForge.scripts.postreg_get_database import initialise_db_connection
from DataForge.functions.utils import fetch_all_cards, find_last_entry
from DataForge.scripts.scryfall_scrapper import import_file

load_dotenv()
'''
--------------------------------------------------------------------------------------------------------------------------------------
functions related to the main, arg from the cli
--------------------------------------------------------------------------------------------------------------------------------------
'''
def get_last_id():
    print("Selecting last mtgstock id in the table:")
    conn, cursor = initialise_db_connection()   
    cursor.execute("SELECT mtg_stock_id FROM card_id ORDER BY mtg_stock_id DESC LIMIT 1")
    row = cursor.fetchone()[0] 
    print(f"The last Id is {row}")
    return row

def update_table_id(batch):
    print("Starting update of card_id table from mtgstocks")
    row = get_last_id()  
# Ensure there is at least one row before accessing
    first_entry = (row + 1) if row else 1
    print(f"Starting at index {first_entry}")
    last_entry = int(os.getenv("HIGHEST_VALID_ID"))
    print(f"Last valid indes is {last_entry}")
    asyncio.run(fetch_all_cards(first_entry, last_entry, batch))
    print("card_id table up to date")
    return None

def get_number_row():
     print("Getting number rows in card_id:")
     conn, cursor = initialise_db_connection()
     cursor.execute("SELECT COUNT(*) FROM card_id")
     row_count = cursor.fetchone()[0]
     print(f"The card_id table as {row_count} entries")
     return row_count

def get_last_valide_index():
    
    try:
        print("Getting las card_id:")
        last_valid = asyncio.run(find_last_entry( get_last_id()))
        print(f"The last valid id {last_valid}")
        return last_valid
    except Exception as e:
        print("Error fetching th last valid ID:", e)
        return None
    
def update_sets():
    print("Looking for new sets...")
    url = os.path.join(os.getenv("API_SCRYFALL_ENDPOINT", 'sets'))
    import_file(url,  os.path.join(os.getenv("PROJECT_PATH")), "sets/json")
    #download new json file
    #compare sets in json file to database
    #if different, add new sets to database
    #add new sets to sql
    print("sets table up to date.")
    print("Updating set table...")


    
