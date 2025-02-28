
from DataForge.functions.utils import sigterm_handler, parse_args
from DataForge.functions.sql_utils import update_table_id, get_number_row, get_last_id
from DataForge.classes.classmodules import Args
from dotenv import load_dotenv
from signal import signal, SIGTERM
from sys import stderr, argv

def main(args : Args):
    load_dotenv()
    if args.update == "c":
       update_table_id(args.x)
    if args.update == "s":
        print("To impplement")
    if args.count:
        get_number_row()
    if args.last:
        get_last_id()
    
def run_cli():
    """Entry point for the command-line tool."""
    signal(SIGTERM, sigterm_handler)
    try:
        args = parse_args(argv[1:]) 
        main(args)
    except KeyboardInterrupt:
        stderr.write("\nExiting the application, g'day!\n")
        exit(1)   

if __name__=="__main__":
    run_cli()

