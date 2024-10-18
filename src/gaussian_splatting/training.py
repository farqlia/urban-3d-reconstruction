from pathlib import Path

import numpy as np
import torch

from src.gaussian_splatting.gradient_measures import GradientMeasure
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


def get_tile_coords(width, height, tile_size):
    h_coords = range(0, height, tile_size)
    w_coords = range(0, width, tile_size)

    return list(itertools.product(h_coords, w_coords))


class GaussianSplatting:

    def __init__(self, scene_folder, output_path, images_folder):
        self.scene_folder = scene_folder
        self.output_path = output_path
        self.images_folder = images_folder

        self.read_reconstruction()
        self.initialize_parameters()

    def initialize_parameters(self):
        self.pcd = o3d.io.read_point_cloud(str(self.scene_folder / 'sparse.ply'))

        self.points = torch.tensor(np.asarray(self.pcd.points), device=device, requires_grad=requires_grad,
                                   dtype=torch.float32)

        # torch.log(colors[0]) - torch.log(1 - colors[0])

        self.colors = torch.tensor(np.asarray(self.pcd.colors), device=device,
                                   dtype=torch.float32)  # colors should also be sigmoid exponents to have range [0, 1]

        self.color_exponents = (torch.log(self.colors) - torch.log(1 - self.colors)).requires_grad_(requires_grad)

        self.covariances = torch.tensor(init_from_uniform(self.points.shape[0], low=0.2, high=0.5), device=device,
                                        dtype=torch.float32)
        self.alphas_exponents_pt = torch.tensor(np.log(np.random.uniform(low=0.1, high=0.3, size=self.points.shape[0])),
                                                requires_grad=requires_grad, device=device, dtype=torch.float32)

        eigenvalues, eigenvectors = torch.linalg.eig(self.covariances)
        self.rot = eigenvectors.real.requires_grad_(requires_grad)

        diagonal = np.array([[1.0, 0, 0], [0, 1.0, 0], [0, 0, 1.0]])

        # Similarly to alphas we'll actually optimize exponents
        scale = torch.sqrt(torch.abs(eigenvalues.real[:, np.newaxis])) * torch.repeat_interleave(
            torch.tensor(diagonal[np.newaxis, ...], device=device), len(self.points), axis=0)
        self.scale_exponents = torch.log(scale).requires_grad_(requires_grad)


    def read_reconstruction(self):
        self.reconstruction = pycolmap.Reconstruction(self.output_path / 'sparse')

    def train_from_perspective(self, image_id, cam_id):
        self.img_rec = self.reconstruction.images[image_id]
        self.cam_id = cam_id
        self.ground_truth_image = mpimg.imread(self.images_folder / f'{self.img_rec.name}')

        self.initialize_parameters_from_camera_perspective()
        self.gradient_measure = GradientMeasure(self.points, self.rot, self.scale_exponents,
                                                self.color_exponents, self.alphas_exponents_pt)

        self._train_tile([400, 150])

    def initialize_parameters_from_camera_perspective(self):
        extrinsic_matrix = get_extrinsic_params(self.img_rec.cam_from_world)
        f, cx, cy = self.reconstruction.cameras[self.cam_id].params
        self.f_pt = torch.scalar_tensor(f, device=device, dtype=torch.float32)
        self.width, self.height = self.reconstruction.cameras[self.cam_id].width, self.reconstruction.cameras[self.cam_id].height
        self.znear, self.zfar = 1, 3
        intrinsic_matrix = get_intrinsic_opengl_params(f, f, self.height, self.width, zfar=self.zfar, znear=self.znear)
        self.W = torch.tensor(extrinsic_matrix[:3, :3].T, device=device, dtype=torch.float32)  # viewing transformation

        self.extrinsic_matrix_pt = torch.tensor(extrinsic_matrix, device=device, dtype=torch.float32)
        self.intrinsic_matrix_pt = torch.tensor(intrinsic_matrix, device=device, dtype=torch.float32)

        self.image_pt = torch.tensor(self.ground_truth_image / 255.0, device=device)


    def train(self):
        pass


    def test_train(self, tile_coords, image_id=1, cam_id=1):
        self.set_training_params()
        self.img_rec = self.reconstruction.images[image_id]
        self.cam_id = cam_id
        self.ground_truth_image = mpimg.imread(self.images_folder / f'{self.img_rec.name}')

        self.initialize_parameters_from_camera_perspective()
        self.gradient_measure = GradientMeasure(self.points, self.rot, self.scale_exponents,
                                                self.color_exponents, self.alphas_exponents_pt)

        self._train_tile(tile_coords)


    def set_training_params(self):
        self.optimizer = torch.optim.Adam([self.points, self.rot, self.scale_exponents,
                                           self.color_exponents, self.alphas_exponents_pt], lr=0.1)
        self.iterations = 2
        self.tile_size = 64

    def to_2d_perspective_and_filter(self, tile_left_lower, tile_upper_right):
        homogeneous_points = convert_to_homogenous(self.points)
        camera_coordinates = homogeneous_points @ self.extrinsic_matrix_pt.T
        clip_coordinates = camera_coordinates @ self.intrinsic_matrix_pt.T
        point_ids = cull_coordinates_ids(clip_coordinates, camera_coordinates, zfar=self.zfar, znear=self.znear)
        ndc_coordinates = to_ndc_coordinates(clip_coordinates[point_ids])
        screen_coordinates = to_screen_coordinates(ndc_coordinates, self.width, self.height, self.zfar, self.znear)

        ids = (screen_coordinates[:, 0] > tile_left_lower[0]) & (
                screen_coordinates[:, 1] > tile_left_lower[1]) & (
                      screen_coordinates[:, 0] < tile_upper_right[0]) & (
                      screen_coordinates[:, 1] < tile_upper_right[1])
        splat_indexes = torch.where(ids == True)[0]

        # Gaussians depths may also change so we need to sort it again
        z_sorted = screen_coordinates[splat_indexes, 2].sort()
        z_indices = z_sorted.indices.type(torch.int)
        splat_z_indexes = splat_indexes[z_indices]

        return splat_z_indexes, point_ids, camera_coordinates, screen_coordinates

    def _train_tile(self, tile_coords):

        tile_pixels = torch.tensor(
            list(itertools.product(range(tile_coords[0], tile_coords[0] + self.tile_size), range(tile_coords[1], tile_coords[1] + self.tile_size))),
            device=device
        )

        tile_left_lower, tile_upper_right = tile_coords, np.array([tile_coords[0] + self.tile_size, tile_coords[1] + self.tile_size])

        print(f"Tile: {tile_coords}")
        running_loss = 0

        for pixel in tile_pixels:

            self.gradient_measure.add_pixel_gradient()

            for i in range(self.iterations):
                self.optimizer.zero_grad()

                splat_z_indexes, point_ids, camera_coordinates, screen_coordinates = self.to_2d_perspective_and_filter(
                    tile_left_lower, tile_upper_right
                )

                color = self.render_pixel(pixel, splat_z_indexes, point_ids, camera_coordinates, screen_coordinates)

                loss = torch.sum(torch.abs(color - self.image_pt[pixel[0], pixel[1]]))

                loss.backward()

                self.gradient_measure.accumulate_pixel_gradient(point_ids)

                running_loss += loss.item()

            # print(running_loss)
            running_loss = 0


    def render(self):
        pass

    def test_render(self, tile_coords):
        self.rendered_image = np.ones((self.height, self.width, 3))
        self._render_tile(tile_coords)

    def render_pixel(self, pixel, splat_z_indexes, point_ids, camera_coordinates, screen_coordinates):

        assert point_ids.shape[0] == self.alphas_exponents_pt.shape[0]
        assert splat_z_indexes.shape[0] <= self.alphas_exponents_pt[point_ids].shape[0]

        alphas = torch.sigmoid(self.alphas_exponents_pt[point_ids][splat_z_indexes]).type(torch.float32)

        saturation_depth = saturate(alphas)

        splat_indexes_f = splat_z_indexes[:saturation_depth]

        splat_rot = self.rot[point_ids][splat_indexes_f]
        splat_scale = torch.exp(self.scale_exponents[point_ids][splat_indexes_f]).type(torch.float32)
        splat_rs = torch.bmm(splat_rot, splat_scale)

        splat_covs = torch.bmm(splat_rs, splat_rs.transpose(1, 2))

        Js = JacobianOps.apply
        jacobians = Js(camera_coordinates[splat_indexes_f], self.f_pt)

        W_splats = torch.repeat_interleave(self.W[torch.newaxis, ...], repeats=len(splat_indexes_f), dim=0)
        M = torch.bmm(jacobians, W_splats)
        proj_covs = torch.bmm(torch.bmm(M, splat_covs), M.transpose(1, 2))[:, :2, :2]

        projs_inv = torch.linalg.inv(proj_covs)

        pixel_pt = torch.repeat_interleave(pixel[torch.newaxis, ...], repeats=len(splat_indexes_f), dim=0)

        diff = (pixel_pt - screen_coordinates[splat_indexes_f, :2])[:, :, torch.newaxis]
        H = torch.bmm(diff.transpose(1, 2), projs_inv)
        g_vals = torch.exp(-1 / 2 * torch.bmm(H, diff)).reshape(len(splat_indexes_f))

        weights = alphas[:saturation_depth] * g_vals
        color = weights.reshape(1, saturation_depth) @ torch.sigmoid(self.color_exponents[point_ids][splat_indexes_f])

        return color


    def _render_tile(self, tile_coords):

        tile_pixels = torch.tensor(
            list(itertools.product(range(tile_coords[0], tile_coords[0] + self.tile_size),
                                   range(tile_coords[1], tile_coords[1] + self.tile_size))),
            device=device
        )

        tile_left_lower, tile_upper_right = tile_coords, np.array(
            [tile_coords[0] + self.tile_size, tile_coords[1] + self.tile_size])

        for pixel in tile_pixels:

            with torch.no_grad():

                splat_z_indexes, point_ids, camera_coordinates, screen_coordinates = self.to_2d_perspective_and_filter(
                    tile_left_lower, tile_upper_right
                )

                color = self.render_pixel(pixel, splat_z_indexes, point_ids, camera_coordinates, screen_coordinates)
                self.rendered_image[pixel[0], pixel[1], :] = color.cpu()

