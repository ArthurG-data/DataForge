from DataForge.scripts.postreg_get_database import initialise_db_connection
from DataForge.functions.sql_utils import execute_many_query
from DataForge.functions.database_creation_utils import execute_sql_file, populate_sets
import os
from dotenv import load_dotenv

load_dotenv()



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


def main():
    set_schema_path = os.path.join( os.getenv('PROJECT_PATH'),'DataForge', 'schemas','set_schema.sql')
    card_schema_path = os.path.join( os.getenv('PROJECT_PATH'),'DataForge', 'schemas','card_schema.sql')
    connection = initialise_db_connection()
    execute_sql_file(set_schema_path, connection)
    set_json = os.path.join( os.getenv('PROJECT_PATH'), 'assets','sets.json')
    populate_sets(set_json, connection)
    execute_sql_file(card_schema_path, connection)
    connection.close()

if __name__=='__main__':
    main()
