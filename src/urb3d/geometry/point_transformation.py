import math

import numpy as np
import pycolmap

def get_camera_from_image(image: pycolmap.Image):
    return image.cam_from_world


def get_extrinsic_params(camera: pycolmap.Rigid3d):
    return np.concatenate((camera.matrix(), np.array([[0, 0, 0, 1]])))


def get_intrinsic_params(reconstruction: pycolmap.Reconstruction):
    '''
    Assumes that there is only one camera, and it is a PINHOLE camera
    :param reconstruction: reconstruction object
    :return: 3x4 intrinsic matrix
    '''
    f, cx, cy = reconstruction.cameras[1].params
    intrinsic_matrix = np.array([[f, 0, cx, 0], [0, f, cy, 0], [0, 0, 1, 0]])
    return intrinsic_matrix


def get_points_xyz(reconstruction: pycolmap.Reconstruction):
    return np.array([point.xyz for point in reconstruction.points3D.values()])


def points3D_to_np(points) -> np.array:
    return np.array([point.xyz for point in points])


def convert_to_homogenous(points: np.array) -> np.array:
    return np.concatenate((points, np.ones((len(points), 1), np.float32)), axis=1)


def convert_from_homogenous(points):
    x = points[:, 0] / points[:, 2]
    y = points[:, 1] / points[:, 2]
    return x, y


def filter_view_points(img_points: np.array, colors: np.array, width: int, height: int):
    points_ids = np.where((img_points[:, 0] > 0) & (img_points[:, 0] < width) & (img_points[:, 1] > 0) & (img_points[:, 1] < height))[0]
    selected_points = img_points[points_ids]
    selected_colors = colors[points_ids]
    return selected_points, selected_colors


def get_intrinsic_opengl_params(focal_x,
                                focal_y,
                                height,
                                width,
                                znear=0.001,
                                zfar=100.0,
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

    P = np.zeros((4, 4))

    P[0, 0] = 2.0 * znear / (right - left)
    P[1, 1] = 2.0 * znear / (top - bottom)
    P[0, 2] = (right + left) / (right - left)
    P[1, 2] = (top + bottom) / (top - bottom)
    P[3, 2] = -1.0
    P[2, 2] = -zfar / (zfar - znear)  # this is to make depth be in range [0, 1]
    P[2, 3] = -zfar * znear / (zfar - znear)  # this is to make depth be in range [0, 1]
    return P


def cull_coordinates_ids(clip_coordinates, camera_coordinates, zfar, znear):
    clip_ids = ((clip_coordinates[:, 3] < clip_coordinates[:, 0]) & (clip_coordinates[:, 0] < -clip_coordinates[:, 3]) & (
                clip_coordinates[:, 3] < clip_coordinates[:, 1]) & (clip_coordinates[:, 1] < -clip_coordinates[:, 3]) &
                (camera_coordinates[:, 2] <= zfar) & (camera_coordinates[:, 2] >= znear))
    return clip_ids


def to_ndc_coordinates(clip_coordinates):
    '''
    Converts to Normalized Device Coordinates
    :param clip_coordinates:
    :return:
    '''
    ndc_coordinates = np.copy(clip_coordinates[:, :3])
    ndc_coordinates[:, 0] = ndc_coordinates[:, 0] / clip_coordinates[:, 3]
    ndc_coordinates[:, 1] = ndc_coordinates[:, 1] / clip_coordinates[:, 3]
    ndc_coordinates[:, 2] = ndc_coordinates[:, 2] / clip_coordinates[:, 3]
    return ndc_coordinates



def to_screen_coordinates(ndc_coordinates, width, height, zfar, znear):
    x_off, y_off = 0, 0

    screen_coordinates = np.zeros((len(ndc_coordinates), 3))

    screen_coordinates[:, 0] = x_off + 0.5 * (-ndc_coordinates[:, 0] + 1) * width
    screen_coordinates[:, 1] = y_off + 0.5 * (-ndc_coordinates[:, 1] + 1) * height
    screen_coordinates[:, 2] = 0.5 * (zfar - znear) * ndc_coordinates[:, 2] + 0.5 * (zfar + znear)  # can be used to resolve depth
    return screen_coordinates



def to_camera_viewpoint(reconstruction: pycolmap.Reconstruction, img_id: int):
    extrinsic_matrix = get_extrinsic_params(get_camera_from_image(reconstruction.images[img_id]))
    homogenous_points = convert_to_homogenous(get_points_xyz(reconstruction)).T

    projected_to_camera_viewpoint = (extrinsic_matrix @ homogenous_points)



def projection_from_reconstruction(reconstruction: pycolmap.Reconstruction, img_id: int):
    extrinsic_matrix = get_extrinsic_params(get_camera_from_image(reconstruction.images[img_id]))
    intrinsic_matrix = get_intrinsic_params(reconstruction)
    homogenous_points = convert_to_homogenous(get_points_xyz(reconstruction)).T

    projected_to_camera_viewpoint = (extrinsic_matrix @ homogenous_points)
    projected_to_image_plane = (intrinsic_matrix @ projected_to_camera_viewpoint).T

    x, y = convert_from_homogenous(projected_to_image_plane)
    img_points = np.stack((x, y)).T
    c = np.array([p.color for p in reconstruction.points3D.values()]) / 255.0

    return img_points, c


def projection_from_points(reconstruction: pycolmap.Reconstruction, points3D, img_id: int):
    extrinsic_matrix = get_extrinsic_params(get_camera_from_image(reconstruction.images[img_id]))
    intrinsic_matrix = get_intrinsic_params(reconstruction)
    homogenous_points = convert_to_homogenous(points3D_to_np(points3D)).T

    projected_to_camera_viewpoint = (extrinsic_matrix @ homogenous_points)
    projected_to_image_plane = (intrinsic_matrix @ projected_to_camera_viewpoint).T

    x, y = convert_from_homogenous(projected_to_image_plane)
    img_points = np.stack((x, y)).T
    c = np.array([p.color for p in points3D]) / 255.0

    return img_points, c