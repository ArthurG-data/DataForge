import aiohttp, json, os
from DataForge.functions.utils import get_header, create_new_table
from dotenv import load_dotenv
from DataForge.scripts.pymongo_get_database import get_collection

load_dotenv()
PROJECT_ROOT = os.getenv("PROJECT_PATH")


url = "https://api.scryfall.com/sets"

async def download_file(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=get_header())  as response:
            if response.status == 200:
                response = await response.json()
                print(response)
                return response["data"]
            else:
                raise Exception(f"Error wihle downloading set database, {response.status}")
               

async def import_file(url, destination):
    try:
        json_file = await download_file(url)  

        
        with open(destination, 'w', encoding='utf-8') as f:
            json.dump(json_file, f, indent=4)

        print(f"File {destination} successfully replaced with new data")

    except Exception as e:
        print(f"Error downloading from {url} to {destination}: {e}")


def get_set_data():
    collection = get_collection("sets")
    data = collection.find({"digital":False}, {"_id":1, "code":1, "name":1, "release_at":1, "card_count":1,"icon_svg_uri":1 })
    return list(data)

def create_set_table(query):
    try:
        create_new_table(query)
    except Exception as e:
        print("Error creating the set table:", {e})

def update_set_table():
    
query = """
CREATE TABLE IF NOT EXISTS sets (
    id varchar(38) PRIMARY KEY,
    code varchar(5) UNIQUE,
    name VARCHAR(100),
    release_data DATE,
    card_count INT,
    icon_url TEXT
);
"""
    

create_set_table(query)