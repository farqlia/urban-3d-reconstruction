import os

import numpy as np
from matplotlib import image as mpimg
from skimage.transform import downscale_local_mean, resize
from pathlib import Path

input_folder = Path("../data/small_city_road_outside/images")
output_folder = Path("../data/small_city_road_outside-d2x/images")

os.makedirs(output_folder, exist_ok=True)

factor = 2

for img_path in input_folder.iterdir():
    img = mpimg.imread(img_path)
    print(f"Processing image {img_path.name}")
    downscaled = downscale_local_mean(img, (factor, factor, 1))
    mpimg.imsave(output_folder / img_path.name, downscaled)

