from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch

from src.geometry.point_transformation import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from src.splats.splats_utils import *
import itertools
import open3d as o3d

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
requires_grad = True

def convert_to_homogenous(points: torch.Tensor):
    return torch.concatenate((points, torch.ones((len(points), 1), dtype=torch.float32, device=device)), dim=1)

def to_ndc_coordinates(clip_coordinates):
    '''
    Converts to Normalized Device Coordinates
    :param clip_coordinates:
    :return:
    '''
    ndc_coordinates = clip_coordinates[:, :3] / clip_coordinates[:, 3:]
    return ndc_coordinates


def to_screen_coordinates(ndc_coordinates, width, height, zfar, znear):
    x_off, y_off = 0, 0

    screen_coordinates = torch.zeros_like(ndc_coordinates)

    screen_coordinates[:, 0] = x_off + 0.5 * (-ndc_coordinates[:, 0] + 1) * width
    screen_coordinates[:, 1] = y_off + 0.5 * (-ndc_coordinates[:, 1] + 1) * height
    screen_coordinates[:, 2] = 0.5 * (zfar - znear) * ndc_coordinates[:, 2] + 0.5 * (zfar + znear)  # can be used to resolve depth
    return screen_coordinates


# Camera coordinates are used to compute jacobian
# Formula inspired by the series of notebooks on medium
class JacobianOps(torch.autograd.Function):

    @staticmethod
    def forward(ctx, cam_points, focal):
        ctx.save_for_backward(cam_points, focal)

        jacs = torch.zeros(len(cam_points), 3, 3, device=device, dtype=torch.float32)

        jacs[:, 0, 0] = focal / cam_points[:, 2]
        jacs[:, 1, 1] = focal / cam_points[:, 2]
        jacs[:, 0, 2] = -focal * cam_points[:, 0] / (cam_points[:, 2] ** 2)
        jacs[:, 1, 2] = -focal * cam_points[:, 1] / (cam_points[:, 2] ** 2)

        return jacs

    @staticmethod
    def backward(ctx, grad_output):
        """
        In the backward pass we receive a Tensor containing the gradient of the loss
        with respect to the output, and we need to compute the gradient of the loss
        with respect to the input.
        """
        points, focal = ctx.saved_tensors

        grad_points = torch.zeros_like(points)

        grad_points[:, 2] = grad_output[:, 0, 0] * (-focal / points[:, 2] ** 2) + grad_output[:, 1, 1] * (
                    -focal / points[:, 2] ** 2)
        grad_points[:, 2] += grad_output[:, 0, 2] * (2 * focal * points[:, 0] / (points[:, 2] ** 3)) + grad_output[:, 1,
                                                                                                       2] * (
                                         2 * focal * points[:, 1] / (points[:, 2] ** 3))
        grad_points[:, 0] = grad_output[:, 0, 2] * (-focal / (points[:, 2] ** 2))
        grad_points[:, 1] = grad_output[:, 1, 2] * (-focal / (points[:, 2] ** 2))

        return grad_points, None

def saturate(alphas):
    """
    Compute the number of Gaussians to consider until the saturation threshold (1.0) is reached
    :param alphas:
    :return:
    """
    i = 0
    alpha_sum = 0
    while alpha_sum < 1.0 and i < len(alphas):
        alpha_sum += alphas[i]
        i += 1
    return i - 1


def tile_coords(width, height, tile_size):
    h_coords = range(0, height, tile_size)
    w_coords = range(0, width, tile_size)

    return list(itertools.product(h_coords, w_coords))


scene_folder = Path('../data/south-building-d4x')
output_path = scene_folder / 'undistorted_images'
images_folder = scene_folder / 'images'

pcd = o3d.io.read_point_cloud(str(scene_folder / 'sparse.ply'))

points = torch.tensor(np.asarray(pcd.points), device=device, requires_grad=requires_grad, dtype=torch.float32)
colors = torch.tensor(np.asarray(pcd.colors), device=device, requires_grad=requires_grad,
                      dtype=torch.float32)  # colors should also be sigmoid exponents to have range [0, 1]
covariances = torch.tensor(init_from_uniform(points.shape[0], low=0.2, high=0.5), device=device, dtype=torch.float32)
alphas_exponents_pt = torch.tensor(np.log(np.random.uniform(low=0.1, high=0.3, size=points.shape[0])),
                                   requires_grad=requires_grad, device=device, dtype=torch.float32)

reconstruction = pycolmap.Reconstruction(output_path / 'sparse')

img_id = 1
img = reconstruction.images[img_id]
cam_id = 1
image = mpimg.imread(images_folder / f'{img.name}')

extrinsic_matrix = get_extrinsic_params(img.cam_from_world)
f, cx, cy = reconstruction.cameras[cam_id].params
f_pt = torch.scalar_tensor(f, device=device, dtype=torch.float32)
width, height = reconstruction.cameras[cam_id].width, reconstruction.cameras[cam_id].height
znear, zfar = 1, 3
intrinsic_matrix = get_intrinsic_opengl_params(f, f, height, width, zfar=zfar, znear=znear)
W = torch.tensor(extrinsic_matrix[:3, :3].T, device=device, dtype=torch.float32) # viewing transformation

extrinsic_matrix_pt = torch.tensor(extrinsic_matrix, device=device, dtype=torch.float32)
intrinsic_matrix_pt = torch.tensor(intrinsic_matrix, device=device, dtype=torch.float32)

image_pt = torch.tensor(image / 255.0, device=device)

eigenvalues, eigenvectors = torch.linalg.eig(covariances)
rot = eigenvectors.real.requires_grad_(requires_grad)

diagonal = np.array([[1.0, 0, 0], [0, 1.0, 0], [0, 0, 1.0]])

# Similarly to alphas we'll actually optimize exponents
scale = torch.sqrt(torch.abs(eigenvalues.real[:, np.newaxis])) * torch.repeat_interleave(
                torch.tensor(diagonal[np.newaxis, ...], device=device), len(points), axis=0)
scale_exponents = torch.log(scale).requires_grad_(requires_grad)

# Optimizers specified in the torch.optim package
optimizer = torch.optim.Adam([points, rot, scale_exponents, colors, alphas_exponents_pt], lr=0.1)
iterations = 50
tile_size = 16
offset = 200

running_loss = 0

scale_grads = []
alpha_grads = []
rot_grads = []

for tile in tile_coords(tile_size, tile_size, tile_size):

    tile = list(tile)
    tile[0] += 200
    tile[1] += 400

    tile_pixels = torch.tensor(
        list(itertools.product(range(tile[0], tile[0] + tile_size), range(tile[1], tile[1] + tile_size))),
        device=device
    )

    tile_left_lower, tile_upper_right = tile, np.array([tile[0] + tile_size, tile[1] + tile_size])

    print(f"Tile: {tile}")

    for pixel in tile_pixels:

        alpha_grads.append([])
        rot_grads.append([])
        scale_grads.append([])

        print(f"Process pixel {pixel}")

        for i in range(iterations):
            optimizer.zero_grad()

            # points are optimized so we need to refresh calculations
            homogeneous_points = convert_to_homogenous(points)
            camera_coordinates = homogeneous_points @ extrinsic_matrix_pt.T
            clip_coordinates = camera_coordinates @ intrinsic_matrix_pt.T
            point_ids = cull_coordinates_ids(clip_coordinates, camera_coordinates, zfar=zfar, znear=znear)
            ndc_coordinates = to_ndc_coordinates(clip_coordinates[point_ids])
            screen_coordinates = to_screen_coordinates(ndc_coordinates, width, height, zfar, znear)

            ids = (screen_coordinates[:, 0] > tile_left_lower[0]) & (screen_coordinates[:, 1] > tile_left_lower[1]) & (
                    screen_coordinates[:, 0] < tile_upper_right[0]) & (screen_coordinates[:, 1] < tile_upper_right[1])
            splat_indexes = torch.where(ids == True)[0]

            # Gaussians depths may also change so we need to sort it again
            z_sorted = screen_coordinates[splat_indexes, 2].sort()
            z_indices = z_sorted.indices.type(torch.int)
            splat_z_indexes = splat_indexes[z_indices]

            assert point_ids.shape[0] == alphas_exponents_pt.shape[0]
            assert splat_z_indexes.shape[0] <= alphas_exponents_pt[point_ids].shape[0]

            alphas = torch.sigmoid(alphas_exponents_pt[point_ids][splat_z_indexes]).type(torch.float32)

            saturation_depth = saturate(alphas)

            splat_indexes_f = splat_z_indexes[:saturation_depth]

            splat_rot = rot[point_ids][splat_indexes_f]
            splat_scale = torch.exp(scale_exponents[point_ids][splat_indexes_f]).type(torch.float32)
            splat_rs = torch.bmm(splat_rot, splat_scale)

            splat_covs = torch.bmm(splat_rs, splat_rs.transpose(1, 2))

            Js = JacobianOps.apply
            jacobians = Js(camera_coordinates[splat_indexes_f], f_pt)

            W_splats = torch.repeat_interleave(W[torch.newaxis, ...], repeats=len(splat_indexes_f), dim=0)
            M = torch.bmm(jacobians, W_splats)
            proj_covs = torch.bmm(torch.bmm(M, splat_covs), M.transpose(1, 2))[:, :2, :2]

            projs_inv = torch.linalg.inv(proj_covs)

            pixel_pt = torch.repeat_interleave(pixel[torch.newaxis, ...], repeats=len(splat_indexes_f), dim=0)

            diff = (pixel_pt - screen_coordinates[splat_indexes_f, :2])[:, :, torch.newaxis]
            H = torch.bmm(diff.transpose(1, 2), projs_inv)
            g_vals = torch.exp(-1 / 2 * torch.bmm(H, diff)).reshape(len(splat_indexes_f))

            weights = alphas[:saturation_depth] * g_vals
            color = weights.reshape(1, saturation_depth) @ colors[point_ids][splat_indexes_f]

            loss = torch.sum(torch.abs(color - image_pt[pixel[0], pixel[1]]))

            loss.backward()

            # print(f"Alpha gradient: {alphas_exponents_pt.grad[point_ids][splat_indexes_f]}")
            # print(f"Rot gradient: {rot.grad[point_ids][splat_indexes_f]}")
            # print(f"Scale gradient: {scale_exponents.grad[point_ids][splat_indexes_f]}")
            # print(f"Points gradient: {points.grad[point_ids][splat_indexes_f]}")

            alpha_grads[-1].append(torch.sum(
                torch.abs(alphas_exponents_pt.grad[point_ids][splat_indexes_f])).clone().cpu().detach().item())
            rot_grads[-1].append(
                torch.sum(torch.abs(rot.grad[point_ids][splat_indexes_f])).clone().cpu().detach().item())
            scale_grads[-1].append(
                torch.sum(torch.abs(scale_exponents.grad[point_ids][splat_indexes_f])).clone().cpu().detach().item())

            optimizer.step()

            running_loss += loss.item()
            # print(f"[{pixel[0].item(), pixel[1].item()}][{i}] Depth = {saturation_depth} Loss = {loss.item()} Running loss = {running_loss}")

        print(running_loss)
        running_loss = 0
