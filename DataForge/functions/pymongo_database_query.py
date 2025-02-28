from pymongo_get_database import get_collection
from bson.objectid import ObjectId

collection = get_collection()


def get_card_by_field(field, value):
    try:
        card_info = collection.find_one({field, value})
        return card_info
    except Exception as e:
        print("Error fetching field {field} with value {value}")
        return None
    
def get_card_by_id(id):
    try:
        obj_id = ObjectId(id) 
        card_info = collection.find_one({"_id":obj_id})
        return card_info
    except Exception as e:
        print(f"Error fetching document {e}")
        return None

def card_by_name(name):
    try:
        card_info = collection.find({"name":name})
        return card_info
    except Exception as e:
        print(f"Error fetching document {e}")
        return None

def add_one_card(card_document):
    try:
        obj_id = ObjectId(card_document["id"]) 
        result = collection.insert_one({"_id" : obj_id, **card_document})
        return result.inserted_id
    except Exception as e:
        print(f"Error fetching document {e}")
        return None
    
def add_many_card(cards):
    try:
        formatted_cards = [{"_id": ObjectId(card["id"]), **card} for card in cards] 
        result = collection.insert_many(formatted_cards)
        return result.inserted_ids
    except Exception as e:
        print(f"Error inserting documents: {e}")
        return None

def update_one_card(id, new_card):
    try:
        obj_id = ObjectId(id)
        result= collection.replace_one({"_id":obj_id}, new_card)
        if result.matched_count > 0:
            return "Document replaced successfully"
        else:
            return "No document found with the given ID"
    except Exception as e:
        print(f"Error fetching document {e}")
        return None

