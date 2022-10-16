# main.py
# Ip Map
# Pings every ip in the ipv4 address space to see if it responds or not
# Generates a nice map
# WARNING: This program will eat your cpu and ram when saving

# Imports
import json
from functools import reduce
from operator import concat

import image
import threads
from global_methods import flatten_iter, lazy_split, transpose_iter
from ip import IP, ComplexIPrange, IPrange
from typing_ import SettingsError


# Definitions
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


def main(settings: dict) -> None:
    """Main"""

    # Set thread amounts
    thread_amounts = settings["thread_amounts"]
    ping_thread_amount = thread_amounts["ping_thread_amount"]
    load_thread_amount = thread_amounts["load_thread_amount"]
    result_thread_amount = thread_amounts["result_thread_amount"]
    save_thread_amount = thread_amounts["save_thread_amount"]

    # Get last checked ips
    try:
        with open("checked_ranges.txt", 'rt') as file:
            try:
                checked_ranges: ComplexIPrange = eval(file.read())
            except SyntaxError:
                checked_ranges = None
    except FileNotFoundError:
        checked_ranges = None
    
    if checked_ranges == None:
        ping_range = IPrange(IP(0, 0, 0, 0), IP(255, 255, 255, 255), no_stop_sub_1=True)
    else:
        ping_range = checked_ranges.inverted()
    
    # Divide up ranges
    ranges = lazy_split(ping_range, ping_thread_amount)

    # Create ping threads
    ping_thrds = threads.ThreadsList([threads.PingThread(range_, num+1) for num, range_ in enumerate(ranges)])
    
    # Create stats thread
    stats_thrd = threads.StatsThread(ping_thrds)

    # Start threads
    ping_thrds.start()
    stats_thrd.start()
    
    # Wait to end
    input()

    # End threads and get thread results
    stats_thrd.end()
    ping_thrds.end()
    results, pinged_range = transpose_iter(ping_thrds.join())

    results = flatten_iter(results)
    pinged_range = ComplexIPrange(pinged_range)

    # Divide up results
    results_subs = lazy_split(results, result_thread_amount)

    # Get images and pix_maps
    imgs, pix_maps = image.get_img_n_pix_maps(load_thread_amount)

    # Create results threads
    results_thrds = threads.ThreadsList([threads.ResultsThread(result_sub, pix_maps, num+1) for num, result_sub in enumerate(results_subs)])

    # Start threads
    print("Pasting results to images...")
    results_thrds.start()

    # Wait for threads to finish
    results_thrds.join()

    # Create img ang out_num list
    imgs_n_out_nums = [(img, out_num+1) for out_num, img in enumerate(imgs)]

    # Divide up list
    imgs_n_out_nums_subs = lazy_split(imgs_n_out_nums, save_thread_amount)

    # Create save threads
    save_thrds = threads.ThreadsList([threads.SaveThread(imgs_n_out_nums_sub, num+1) for num, imgs_n_out_nums_sub in enumerate(imgs_n_out_nums_subs)])

    # Create stats thread
    stats_thrd = threads.StatsThread(save_thrds)

    # Start threads
    stats_thrd.start()
    save_thrds.start()

    # Wait for threads to finish
    save_thrds.join()
    stats_thrd.end()

    with open("checked_ranges.txt", 'wt') as file:
        file.write(repr(ComplexIPrange(pinged_range.ranges + (checked_ranges.ranges if checked_ranges != None else []))))


# Run
if __name__ == "__main__":
    settings = load_settings()
    main(settings)
