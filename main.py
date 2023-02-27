# main.py
# Ip Mapper
# Pings every ip in the ipv4 address space to see if it responds or not
# Generates a nice map
# WARNING: This program will eat your cpu and ram when saving


# Imports
import src.mapper
import src.reset_submaps
import src.settings
import src.stitch


# Definitions
START_MESSAGE =\
"""Welcome to IP mapper!
Please select one of the following options:
1) Map IPs
2) Stitch Map together
3) Reset all maps
4) Change settings"""


def main() -> None:
    # Print greeting and get command
    print(START_MESSAGE)
    inp = input()

    # Match command and run appropriate script
    match inp:
        
        # Mapper
        case '1':
            settings_ = settings.load_settings()
            mapper.main(settings_)
        
        # Stitch
        case '2':
            stitch.main()
        
        # Reset submaps
        case '3':
            reset_submaps.main()

        # Change settings
        case '4':
            settings.main()
        
        case other:
            print("Invalid command")

# Run
if __name__ == "__main__":
    main()