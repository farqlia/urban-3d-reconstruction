import itertools

import numpy as np
import numpy.linalg as LA
import math

def get_bounding_box(mu, cov, extent=3.0):
    eigenvalues = LA.eigvals(cov) # this can be replaced with torch version
    radius = extent * math.sqrt(abs(eigenvalues.max())) # 3 standard deviations from the center
    bounding_box = np.array([
        mu[0] + radius, # x max
        mu[0] - radius, # x min
        mu[1] + radius, # y max
        mu[1] - radius]) # y min
    return bounding_box

def get_pixel_coords(pixels):
    h, w = pixels.shape[0], pixels.shape[1]
    pixels_coords = np.array(list(itertools.product(range(h), range(w))))
    return np.array(pixels_coords)

def pixels_within_bb_ids(pixels, mu, cov, extent=3.0):
    x_max, x_min, y_max, y_min = get_bounding_box(mu, cov, extent=extent)
    pixels_coords = get_pixel_coords(pixels)
    ids = (pixels_coords[:, 0] < x_max) & (pixels_coords[:, 0] > x_min) & (pixels_coords[:, 1] < y_max) & (pixels_coords[:, 1] > y_min)
    return ids

def init_from_uniform(n, low=0.1, high=0.3):
    covs = np.zeros((n, 3, 3), dtype=np.float32)
    vals = np.random.uniform(low=low, high=high, size=n)
    covs[:, 0, 0] = vals
    covs[:, 1, 1] = vals
    covs[:, 2, 2] = vals
    return covs