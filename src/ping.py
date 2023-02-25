# ping.py
# Just holds the ping methods to keep things clean


# Imports
from ping3 import ping as ping_

from src.ip import IP


# Definitions
def ping(ip: IP):
    """Ping the specified ip"""
    
    try:
        return ping_("{}.{}.{}.{}".format(*tuple(ip)), 2)
    except OSError:
        return False
