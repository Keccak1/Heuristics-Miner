from datetime import datetime
from .dt_type import DtType

def timestamp2dt(timestamp):
    try:
        return datetime.fromtimestamp(timestamp)
    except TypeError:
        try:
            return datetime.fromtimestamp(int(timestamp))    
        except ValueError:
             raise ValueError(f"Cannot cast: {timestamp} to valid timestamp")
    except ValueError:
        raise ValueError(f"Not valid timestamp: {timestamp}")
    
def string2dt(date_text, pattern):
    try:
        return datetime.strptime(date_text, pattern)
    except ValueError:
        raise ValueError(f"Not valid datetime pattern: {pattern} for: {date_text}")
    
def _2dt(dt,dt_type, pattern=""):
    if dt_type == DtType.TIMESTAMP:
        return timestamp2dt(dt)
    
    elif dt_type == DtType.TEXT:
        return string2dt(dt, pattern)
    
    else:
        raise TypeError(f"Unexpected type of DtType pattern: {dt}")
