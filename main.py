# main.py
# Ip Mapper
# Pings every ip in the ipv4 address space to see if it responds or not
# Generates a nice map
# WARNING: This program will eat your cpu and ram when saving


# Definitions
START_MESSAGE = """Welcome to IP mapper!
Please select one of the following options:
1) Map IPs
2) Stitch Map together
3) Reset all maps
4) Change settings"""


def main() -> None:
    print(START_MESSAGE)
    