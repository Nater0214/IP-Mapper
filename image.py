# image.py
# Holds methods for reading and writing to the maps.


# Imports
from PIL import Image
from PIL.PngImagePlugin import PngImageFile
from PIL.PyAccess import PyAccess

import threads
from global_methods import flatten_iter, lazy_split
from ip import IP


# Definitions
def get_images() -> list[PngImageFile]:
    """Returns all 64 image objects"""

    return [Image.open(f".\\maps\\map{i}.png") for i in range(1, 65)]


def get_pix_maps(imgs: list[PngImageFile], load_thread_amount: int) -> list[PyAccess]:
    """Returns all 64 pixel access objects from a list of images"""

    # Split images
    imgs_subs = lazy_split(imgs, load_thread_amount)

    # Create load threads
    load_thrds = threads.ThreadsList([threads.LoadThread(imgs_sub, num+1) for num, imgs_sub in enumerate(imgs_subs)])

    # Create stats thread
    stats_thrd = threads.StatsThread(load_thrds)
    
    # Start threads
    stats_thrd.start()
    load_thrds.start()

    # Get thread result and return
    out = flatten_iter(load_thrds.join())
    stats_thrd.end()
    stats_thrd.join()
    return out


def get_img_n_pix_maps(load_thread_amount: int) -> tuple[list[PngImageFile], list[PyAccess]]:
    """Return all image and pixel access objects
    
    Short code for:
    >>> import img
    >>> imgs, pix_maps = img.get_images(), img.get_pix_maps()"""

    return (imgs := get_images()), get_pix_maps(imgs, load_thread_amount)


def write_pix(pix_maps: list[PyAccess], result: tuple[IP, bool]) -> None:
    """Writes the ping result to the pixel access objects"""

    # Initialize vars
    ip, response = result
    out_img = 1
    a, b, c, d = tuple(ip)

    # Set out image
    while True:
        if a in range(32):
            break
        else:
            a -= 32
            out_img += 1

    while True:
        if c in range(32):
            break
        else:
            c -= 32
            out_img += 8

    # Set coordinates
    x, y = (a*256)+b, (c*256)+d

    # Write to pixel map
    pix_maps[out_img-1][x, y] = (255, 255, 255) if response else (0, 0, 0)


def save(img: PngImageFile, out_num: int) -> None:
    """Save pix_maps to their images"""

    img.save(f"maps\\map{out_num}.png")


if __name__ == "__main__":
    pass
