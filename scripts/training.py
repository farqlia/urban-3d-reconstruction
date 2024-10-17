from pathlib import Path

import matplotlib.pyplot as plt

from src.gaussian_splatting.training import GaussianSplatting

scene_folder = Path('../data/south-building-d4x')
output_path = scene_folder / 'undistorted_images'
images_folder = scene_folder / 'images'

gaussian_splatting = GaussianSplatting(scene_folder, output_path, images_folder)
gaussian_splatting.train()

gaussian_splatting.render()

plt.imshow(gaussian_splatting.ground_truth_image)
plt.show()
plt.imshow(gaussian_splatting.rendered_image)
plt.show()

gaussian_splatting.gradient_measure.plot_gradient_stats()