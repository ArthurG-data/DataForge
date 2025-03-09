from DataForge.functions.sql_utils import execute_many_query
import uuid, json

def prepare_insert_query(table_name, columns):
    """
    Generates an INSERT query with placeholders for bulk insertion.

    Args:
        table_name (str): The name of the table to insert into.
        columns (list): A list of column names.
        values (list of tuples): Data to be inserted.

    Returns:
        str: The SQL query string.
        list of tuples: The values to be inserted.
    """
    placeholders = ", ".join(["%s"] * len(columns))  # Creates "%s, %s, ..." dynamically
    column_names = ", ".join(columns)
    query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
    return query

#query related to the sets tables
populate_set_type_query="""
INSERT INTO set_type_list (set_type_id, set_type) 
VALUES (%s, %s)
ON CONFLICT (set_type) DO NOTHING
"""
populate_set_query="""
INSERT INTO sets (set_id, set_name, set_code, set_type_id, released_at, digital)
VALUES (%s, %s, %s, %s, %s, %s)
"""
populate_source_list="""
INSERT INTO set_url_source_list(source_id, url_source)
VALUES (%s, %s)
"""
populate_url="""
INSERT INTO set_url(set_id, source_id, uri)
VALUES (%s,%s, %s)
"""
drop_set_query="""
DROP TABLE IF EXISTS sets, set_type_list, set_url_source_list, set_url CASCADE;
"""

def prepare_set_type_queries(json_data):
    """Prepares the unique set_type insert queries."""
    set_type_data = {}
    for entry in json_data:
        set_type = entry.get("set_type", "none")  # Default to 'none' if missing
        if set_type not in set_type_data:
            set_type_data[set_type] = str(uuid.uuid4())
    values = [(set_id, set_type) for set_type, set_id in set_type_data.items()]
    return set_type_data, values 


def prepare_set_queries(json_data, set_type_data):
    """Prepares the set insert queries."""
    set_data = []
    for entry in json_data:
        set_id = entry.get("id")
        set_name = entry.get("name")
        set_code = entry.get("code")
        released_at = entry.get("released_at")
        digital = entry.get("digital", False)
        set_type_id = set_type_data.get(entry.get("set_type", "none"))
        set_data.append((set_id, set_name, set_code, set_type_id, released_at, digital))
    return set_data

def prepare_url_source_list():
    uri_keys = ["uri", "scryfall_uri", "search_uri", "icon_svg_uri"]
    table_entry = []
    source_dict = {}
    for entry in uri_keys:
        source_id = str(uuid.uuid4())
        table_entry.append((source_id, entry))
        source_dict[entry] = source_id
    return table_entry, source_dict
    
def prepare_set_url_queries(json_data, source_dict):
    """Prepares the set_url insert queries."""
    uri_keys = ["uri", "scryfall_uri", "search_uri", "icon_svg_uri"]
    set_url_data = []

    for entry in json_data:
        set_id = entry.get("id") 
        for key in uri_keys:
            url_value = entry.get(key)
            if url_value:
                set_url_data.append((set_id,source_dict[key], url_value))

    return set_url_data

def execute_sql_file(filename, connection):
    with open(filename, "r") as file:
        sql = file.read()
    
    try:
        # Connect to PostgreSQL
        cur = connection.cursor()
        
        # Execute SQL commands
        cur.execute(sql)
        connection.commit()
        
        print("Database schema created successfully!")
    
    except Exception as e:
        print("Error:", e)
    
    finally:
        cur.close()

def populate_sets(set_json, connection):
    with open(set_json ,'r' ,encoding='utf-8') as file:
        data = json.load(file)
    set_type_data_dict, value = prepare_set_type_queries(data)
    set_data = prepare_set_queries(data, set_type_data_dict)
    url_list, url_dict = prepare_url_source_list()
    set_url = prepare_set_url_queries(data, url_dict)
    try:
        execute_many_query(populate_set_type_query,value, connection)
        execute_many_query(populate_set_query,set_data, connection)
        execute_many_query(populate_source_list,url_list, connection)
        execute_many_query(populate_url,set_url, connection)
        connection.commit()
        print('Sets table successfullt populated')
    except Exception as e:
        print('Error populatin the sets tables: ', e)
        connection.rollback()

