import os

import numpy as np
from matplotlib import image as mpimg
from skimage.transform import downscale_local_mean, resize
from pathlib import Path

input_folder = Path("../data/south-building/images")
output_folder = Path("../data/south-building/images_downsampled")

os.makedirs(output_folder, exist_ok=True)

factor = 4

for img_path in input_folder.iterdir():
    img = mpimg.imread(img_path)
    print(f"Processing image {img_path.name}")
    downscaled = downscale_local_mean(img, (factor, factor, 1)).astype(np.uint8)
    mpimg.imsave(output_folder / img_path.name, downscaled)

