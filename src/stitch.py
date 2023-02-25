# stitch.py
# Stitches all the images together to make one big map


# Imports
from PIL import Image

from src.image import get_images
from src.listb1 import Listb1


# Definitions
def main() -> None:
    # Open all the images
    imgs = Listb1(get_images())

    # Initialize big map
    big_map = Image.new('RGB', (65536, 65536))

    # Paste sub-maps to big map
    print("Pasting sub-maps...")
    for i, y in enumerate(range(0, 64, 8)):
        for j, x in enumerate(range(1, 9)):
            big_map.paste(imgs[x + y], (8192*i, 8192*j))

    # Save the big map
    print("Saving map...")
    big_map.save("map.png")

# Run
if __name__ == "__main__":
    main()