
import os, asyncio

from database_manager.scripts.postreg_get_database import initialise_db_connection
from database_manager.functions.utils import fetch_all_cards

'''
--------------------------------------------------------------------------------------------------------------------------------------
functions related to the main
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

def get_number_row():
     print("Getting number rows in card_id:")
     conn, cursor = initialise_db_connection()
     cursor.execute("SELECT COUNT(*) FROM card_id")
     row_count = cursor.fetchone()[0]
     print(f"The card_id table as {row_count} entries")
     return row_count

