# settings.py
# For changing settings


# Imports
import json
from sys import exit as sys_exit


# Definitions
START_MESSAGE = """Change settings
1) Use default settings
2) Change thread amounts
3) Save and exit"""


def load_settings() -> dict:
    """Load the settings from the json"""

    # Get json data
    with open("settings.json", 'rt') as file:
        json_data = json.load(file)
    
    # Return settings
    return json_data
    

def main():
    settings = load_settings()
    while True:
        # Print start amount and get command
        print(START_MESSAGE)
        inp = input()

        # Match command
        match inp:
            
            # Default settings
            case '1':
                # Print message
                print(f"Currently using {'user' if not settings['default_settings'] else 'default'} settings.")
                
                # Get toggle y/n
                while True:
                    inp = input("Toggle this? (y/n) ")
                    
                    match inp.lower():
                        case 'y':
                            settings['default_settings'] = not settings['default_settings']
                            break
                        case 'n':
                            break
                        case other:
                            print("What?")
                    
                    print()
            
            # Thread amounts
            case '2':
                # Print message
                thread_amounts = settings["user_defined"]["thread_amounts"]
                print(f"Current user defined thread amounts are:\nPing: {thread_amounts['ping']}\nLoad: {thread_amounts['load']}\nResult: {thread_amounts['result']}\nSave: {thread_amounts['save']}")

                while True:
                    inp = input("Input the name of the amount you want to change, followed with a space by the amount: ")
                    
                    cmd = inp.split(' ')
                    cmd[0] = cmd[0].lower()
                    if len(cmd) == 2:
                        cmd[1] = int(cmd[1])
                    
                    nvm = False
                    match cmd:
                        case ['ping', num]:
                            thread_amounts['ping'] = num
                            break
                        
                        case ['load', num]:
                            thread_amounts['load'] = num
                            break
                        
                        case ['result', num]:
                            thread_amounts['result'] = num
                            break
                        
                        case ['save', num]:
                            thread_amounts['save'] = num
                            break
                        
                        case ['nvm']:
                            print("Okay!")
                            nvm = True
                            break
                        
                        case other:
                            print("What?")
                
                if not nvm:
                    print(f"Changed {cmd[0].capitalize()} to {cmd[1]}")
                    settings["user_defined"]["thread_amounts"] = thread_amounts
            
            # Save and exit
            case '3':
                with open("settings.json", 'wt') as file:
                    json.dump(settings, file)
                
                sys_exit()
        
        print()


# Run
if __name__ == '__main__':
    main()