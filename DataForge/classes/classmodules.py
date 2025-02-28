from typing import Optional, NamedTuple

class Args(NamedTuple):
    last: Optional[int]
    count: bool
    update: bool
    verbose: bool
    quiet: bool
    x: int  
