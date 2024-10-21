import math

import numpy as np
import pycolmap
import torch


def convert_to_homogenous(points: torch.Tensor, device=torch.device('cpu')) -> torch.Tensor:
    return torch.concatenate((points, torch.ones((len(points), 1))), dim=1).type(torch.float32).to(device)

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


def get_extrinsic_params(camera: pycolmap.Rigid3d, device=torch.device('cpu')):
    return torch.concatenate((torch.tensor(camera.matrix()), torch.tensor([[0, 0, 0, 1]]))).to(device).type(torch.float32)

def get_intrinsic_opengl_params(focal_x,
                                focal_y,
                                height,
                                width,
                                znear=0.001,
                                zfar=100.0,
                                device=torch.device('cpu')
                                ):
    """
    Gets the internal perspective projection matrix

    znear: near plane (set by user)
    zfar: far plane (set by user)
    fovX: field of view in x, calculated from the focal length
    fovY: field of view in y, calculated from the focal length
    """
    # https://stackoverflow.com/questions/39992968/how-to-calculate-field-of-view-of-the-camera-from-camera-intrinsic-matrix
    fov_x = np.array([2 * math.atan(width / (2 * focal_x))])
    fov_y = np.array([2 * math.atan(height / (2 * focal_y))])

    tan_half_foc_x = math.tan((fov_x / 2))
    tan_half_foc_y = math.tan((fov_y / 2))

    top = tan_half_foc_y * znear
    bottom = -top
    right = tan_half_foc_x * znear
    left = -right

    P = torch.zeros((4, 4))

    P[0, 0] = 2.0 * znear / (right - left)
    P[1, 1] = 2.0 * znear / (top - bottom)
    P[0, 2] = (right + left) / (right - left)
    P[1, 2] = (top + bottom) / (top - bottom)
    P[3, 2] = -1.0
    P[2, 2] = -zfar / (zfar - znear)  # this is to make depth be in range [0, 1]
    P[2, 3] = -zfar * znear / (zfar - znear)  # this is to make depth be in range [0, 1]
    return P.to(device).type(torch.float32)
