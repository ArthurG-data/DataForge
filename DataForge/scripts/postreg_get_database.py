from dotenv import load_dotenv
import os, psycopg2

load_dotenv()

host = os.getenv("POSTGRES_HOST")
dbname = os.getenv("DBNAME")
password = os.getenv("POSTGRES_PASSWORD")
user = os.getenv("POSTGRES_USER")

params = f"host={host} dbname={dbname} user={user} password={password} port='5432'"


def get_postgres_params():
    return params

def initialise_db_connection():
    """
    function: Initialise a connection with a posterSQL server
    input: parameters to initilise the cponnection. Is a string of the format "params='value'" with host, dbname, user, password, port
    output: connector and cursor
    """
    conn = psycopg2.connect(
    get_postgres_params())
    cursor = conn.cursor()
    return conn, cursor

if __name__=="__main__":
    conn, cursor = initialise_db_connection()