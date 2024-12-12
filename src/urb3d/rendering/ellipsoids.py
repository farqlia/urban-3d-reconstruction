import numpy as np
from scipy.spatial.transform import Rotation as R

class Ellipsoid:
    def __init__(self, position, radii, color, quats=None):
        self.position = np.array(position, dtype=np.float32)  # Position of the ellipsoid in 3D space
        self.radii = radii                                    # Radii for x, y, z directions
        self.color = color                                      # Color of the ellipsoid

        if quats:
            self.prepare_rot_matrix(quats)
        else:
            self.rotation_matrix = np.identity(3).astype(np.float32)

    def prepare_rot_matrix(self, quats):
        self.rotation_matrix = R.from_quat(quats).as_matrix()

    def rotate_X(self, angle):
        self.rotation_matrix = np.identity(3)
        self.rotation_matrix[1, 1] = np.cos(angle)
        self.rotation_matrix[2, 2] = np.cos(angle)
        self.rotation_matrix[1, 2] = -np.sin(angle)
        self.rotation_matrix[2, 1] = np.sin(angle)

    def rotate_Y(self, angle):
        self.rotation_matrix = np.identity(3)
        self.rotation_matrix[0, 0] = np.cos(angle)
        self.rotation_matrix[0, 2] = np.sin(angle)
        self.rotation_matrix[2, 0] = -np.sin(angle)
        self.rotation_matrix[2, 2] = np.cos(angle)

    def rotate_Z(self, angle):
        self.rotation_matrix = np.identity(3)
        self.rotation_matrix[0, 0] = np.cos(angle)
        self.rotation_matrix[0, 1] = -np.sin(angle)
        self.rotation_matrix[1, 0] = np.sin(angle)
        self.rotation_matrix[1, 1] = np.cos(angle)



# https://stackoverflow.com/questions/7687148/drawing-sphere-in-opengl-without-using-glusphere
# Helper function to generate vertices and indices for an ellipsoid
def generate_ellipsoid_vertices(a, b, c, latitude_bands, longitude_bands):
    vertices = []
    indices = []
    for lat in range(latitude_bands + 1):
        theta = lat * np.pi / latitude_bands
        sin_theta = np.sin(theta)
        cos_theta = np.cos(theta)

        for lon in range(longitude_bands + 1):
            phi = lon * 2 * np.pi / longitude_bands
            sin_phi = np.sin(phi)
            cos_phi = np.cos(phi)

            x = a * cos_phi * sin_theta
            y = b * cos_theta
            z = c * sin_phi * sin_theta
            vertices.extend([x, y, z])

            if lat < latitude_bands and lon < longitude_bands:
                first = lat * (longitude_bands + 1) + lon
                second = first + longitude_bands + 1
                indices.extend([first, second, first + 1, second, second + 1, first + 1])

    return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)