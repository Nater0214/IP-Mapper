# reset_submaps.py
# Resets all the submaps


# Imports
from PIL import Image

import src.settings as settings
import src.threads as threads
from src.global_methods import lazy_split


# Definitions
def main() -> None:
    print("Creating images...")
    imgs = [Image.new(mode='RGB', size=(8192,8192), color=(18,18,18)) for _ in range(64)]

    # Create img and out_num list
    imgs_n_out_nums = [(img, out_num+1) for out_num, img in enumerate(imgs)]

    # Divide up list
    settings_ = settings.load_settings()
    thrd_amount = 0
    if settings_["default_settings"]:
        thrd_amount = settings_["default"]["thread_amounts"]["save"]
    else:
        thrd_amount = settings_["user_defined"]["thread_amounts"]["save"]
    
    imgs_n_out_nums_subs = lazy_split(imgs_n_out_nums, thrd_amount)

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

    # Reset checked ranges
    with open("checked_ranges.txt", 'wt') as file:
        file.write("None")


# Run
if __name__ == '__main__':
    main()