from typing import Optional, NamedTuple

class Args(NamedTuple):
    '''
    a class to pass the arg of the cli to the main function
    '''
    last: Optional[str]
    count: bool
    update: Optional[str]
    verbose: bool
    quiet: bool
    x: int  

