import numpy as np
import point_cloud_utils as pcu

SH_C0 = 0.28209479177387814
SH_C1 = 0.4886025119029199
SH_C2 = [1.0925484305920792,
        -1.0925484305920792,
        0.31539156525252005,
        -1.0925484305920792,
        0.5462742152960396
]
SH_C3 = [
    -0.5900435899266435,
    2.890611442640554,
    -0.4570457994644658,
    0.3731763325901154,
    -0.4570457994644658,
    1.445305721320277,
    -0.5900435899266435
]

# .ply model path
def compute_normals(model_path):
    # sensor_dirs are stored in the normal channel and are encoded as unit
    # vectors pointing from the point to the scanner
    pts, sensor_dirs = pcu.load_mesh_vf(model_path)

    # Optionally delete point whose normal is at an oblique (greather than 85 degree) angle with the sensor direction
    drop_angle = np.deg2rad(85.0)

    # Size of the neighborhood used for each point
    num_nbrs = 32

    # n are the fitted normals
    # n_idx are used to delete points which were filterd (ignore this if you don't pass in drop_angle)
    _, n = pcu.estimate_point_cloud_normals_knn(pts, num_nbrs, view_directions=sensor_dirs)
    return n

def sh_to_rgb(points, normals):
    p = normals
    x = p[:, [0]]
    y = p[:, [1]]
    z = p[:, [2]]

    sh_n = len([x for x in points.columns if x.startswith('sh')])

    sh0s = SH_C0 * points[['sh0_x', 'sh0_y', 'sh0_z']].values
    res = sh0s

    if sh_n > 3:

        sh1s = SH_C1 * (
                    -y * points[['sh1_x', 'sh1_y', 'sh1_z']].values + z * points[['sh2_x', 'sh2_y', 'sh2_z']].values - x *
                    points[['sh3_x', 'sh3_y', 'sh3_z']].values)

        res += sh1s

        if sh_n > 12:

            xx = p[:, [0]] ** 2
            yy = p[:, [1]] ** 2
            zz = p[:, [2]] ** 2
            xy = x * y
            xz = x * z
            yz = y * z
            sh2s = SH_C2[0] * xy * points[['sh4_x', 'sh4_y', 'sh4_z']].values + SH_C2[1] * yz * points[
                ['sh5_x', 'sh5_y', 'sh5_z']].values + SH_C2[2] * (2 * zz - xx - yy) * points[
                       ['sh6_x', 'sh6_y', 'sh6_z']].values + SH_C2[3] * xz * points[['sh7_x', 'sh7_y', 'sh7_z']].values + SH_C2[
                       4] * (xx - yy) * points[['sh8_x', 'sh8_y', 'sh8_z']].values

            res += sh2s

            if sh_n > 27:

                sh3s = SH_C3[0] * y * (3. * xx - yy) * points[['sh9_x', 'sh9_y', 'sh9_z']].values + SH_C3[1] * xy * z * points[
                    ['sh10_x', 'sh10_y', 'sh10_z']].values + SH_C3[2] * y * (4. * zz - xx - yy) * points[
                           ['sh11_x', 'sh11_y', 'sh11_z']].values + SH_C3[3] * z * (2.0 * zz - 3.0 * xx - 3.0 * yy) * points[
                           ['sh12_x', 'sh12_y', 'sh12_z']].values + SH_C3[4] * x * (4.0 * zz - xx - yy) * points[
                           ['sh13_x', 'sh13_y', 'sh13_z']].values + SH_C3[5] * z * (xx - yy) * points[
                           ['sh14_x', 'sh14_y', 'sh14_z']].values + SH_C3[6] * x * (xx - 3.0 * yy) * points[
                           ['sh15_x', 'sh15_y', 'sh15_z']].values

                res += sh3s

    return np.where(res > 0, res, 0)


def enrich(ptcld, colors):
    ptcld.points.loc[:, 'red'] = np.clip(colors[:, 0], 0, 1)
    ptcld.points.loc[:, 'green'] = np.clip(colors[:, 1], 0, 1)
    ptcld.points.loc[:, 'blue'] = np.clip(colors[:, 2], 0, 1)
