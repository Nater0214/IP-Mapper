from PIL import Image

import threads
from global_methods import lazy_split

imgs = [Image.new(mode='RGB', size=(8192,8192)) for i in range(64)]

# Create img ang out_num list
imgs_n_out_nums = [(img, out_num+1) for out_num, img in enumerate(imgs)]

# Divide up list
imgs_n_out_nums_subs = lazy_split(imgs_n_out_nums, 32)

# Create save threads
save_thrds = threads.ThreadsList([threads.SaveThread(imgs_n_out_nums_sub, num+1) for num, imgs_n_out_nums_sub in enumerate(imgs_n_out_nums_subs)])

# Start threads
save_thrds.start()

# Wait for threads to finish
save_thrds.join()
