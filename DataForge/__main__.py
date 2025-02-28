
from functions.utils import sigterm_handler, parse_args
from functions.sql_utils import update_table_id, get_number_row, get_last_id
from classes.classmodules import Args
from dotenv import load_dotenv
from signal import signal, SIGTERM
from sys import stderr

def main(args : Args):
    load_dotenv()
    if args.update:
       update_table_id(args.x)
    if args.count:
        get_number_row()
    if args.last:
        get_last_id()
    
   

if __name__=="__main__":
    signal(SIGTERM, sigterm_handler)
    try:
        args = parse_args()

        main(args)
    except KeyboardInterrupt:
        stderr.write("Exiting the application, g'day")
        exit(1)

