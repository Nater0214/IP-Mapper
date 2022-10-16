# main.py
# Ip Map
# Pings every ip in the ipv4 address space to see if it responds or not
# Generates a nice map
# WARNING: This program will eat your cpu and ram when saving

# Imports
from functools import reduce
from operator import concat

import image
import threads
from global_methods import flatten_iter, lazy_split, transpose_iter
from ip import IP, ComplexIPrange, IPrange
from typing_ import SettingsError


# Settings
PING_THREAD_AMOUNT = 4
RESULT_THREAD_AMOUNT = 16
LOAD_THREAD_AMOUNT = 32
SAVE_THREAD_AMOUNT = 32


# Check settings validity
if LOAD_THREAD_AMOUNT > 64:
    raise SettingsError("LOAD_THREAD_AMOUNT cannot be more than 64")

if SAVE_THREAD_AMOUNT > 64:
    raise SettingsError("SAVE_THREAD_AMOUNT cannot be more than 64")


# Definitions
def main() -> None:
    # Get last checked ips
    with open("checked_ranges.txt", 'rt') as file:
        try:
            checked_ranges: ComplexIPrange = eval(file.read())
        except SyntaxError:
            checked_ranges = None
    
    if checked_ranges == None:
        ping_range = IPrange(IP(0, 0, 0, 0), IP(255, 255, 255, 255), no_stop_sub_1=True)
    else:
        ping_range = checked_ranges.inverted()
    
    # Divide up ranges
    ranges = lazy_split(ping_range, PING_THREAD_AMOUNT)

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
    results_subs = lazy_split(results, RESULT_THREAD_AMOUNT)

    # Get images and pix_maps
    imgs, pix_maps = image.get_img_n_pix_maps(LOAD_THREAD_AMOUNT)

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
    imgs_n_out_nums_subs = lazy_split(imgs_n_out_nums, SAVE_THREAD_AMOUNT)

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
    main()