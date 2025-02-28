from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection_string():
    return os.getenv("ULI")

def get_collection(collection):
    client = MongoClient(get_connection_string(), 
        minPoolSize = 50,
        maxPoolSize = 250,
    )
    db = client.get_database("card_info")
    collection = db[collection]

    return collection

if __name__ == "__main__":

    collection = get_collection()
