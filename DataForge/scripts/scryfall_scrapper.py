import aiohttp, json
from DataForge.functions.utils import get_header, create_new_table
from psycopg2.extras import execute_values
from DataForge.scripts.pymongo_get_database import get_collection
from DataForge.scripts.postreg_get_database import initialise_db_connection


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

def migrate_mongo_to_postgres():
    """
    migrate the set symbols from mongoDB set to sql
    """

    collection = get_collection('sets')
    mongo_data = collection.find(
            {"digital": False},  # Filtering condition
        {"_id": 1, "code": 1, "name": 1, "released_at": 1, "card_count": 1, "icon_svg_uri": 1}  # Fields to extract
    )

    conn, cursor = initialise_db_connection()
    INSERT_QUERY = """
    INSERT INTO sets (id, code, name, release_data, card_count, icon_url)
    VALUES %s
    ON CONFLICT (id) DO NOTHING;
    """
    list_data = list(mongo_data)
    rows = [(str(item["_id"]), item["code"], item["name"], item["released_at"], item.get("card_count", 0), item["icon_svg_uri"])
            for item in list_data]
    try:
        execute_values(cursor, INSERT_QUERY, rows)
        conn.commit()

        print(f"Number of sets added: {len(rows)}")
    except Exception as e:
        print("Could not update sets table:", e)
    finally:
        cursor.close()
        conn.close()


