# settings.py
# For changing settings


# Imports
import json


# Definitions
START_MESSAGE = """Change settings
1) Use default settings
2) Change thread amounts
3) Exit"""


def load_settings() -> dict:
    """Load the settings from the json"""

    # Get json data
    with open("settings.json", 'rt') as file:
        json_data = json.load(file)
    
    # Return settings
    if json_data["default_settings"]:
        return json_data["default"]
    else:
        return json_data["user_defined"]
    

def main():
    while True:
        # Print start amount and get command
        print(START_MESSAGE)
        inp = input()

        # Match command
        match inp:
            case '1':
                


# Run
if __name__ == '__main__':
    load_settings()
    main()