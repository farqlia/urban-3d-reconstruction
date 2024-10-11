import pycolmap
from src.geometry.point_transformation import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import argparse
from pathlib import Path

def project_image(reconstruction_path, img_id, cam_id):
    reconstruction = pycolmap.Reconstruction(reconstruction_path)
    img = reconstruction.images[img_id]

    points = np.array([point.xyz for point in reconstruction.points3D.values()])
    colors = np.array([point.color / 255. for point in reconstruction.points3D.values()])

    extrinsic_matrix = get_extrinsic_params(img.cam_from_world)
    f, _, _ = reconstruction.cameras[cam_id].params
    width, height = reconstruction.cameras[cam_id].width, reconstruction.cameras[cam_id].height
    znear, zfar = 1, 5
    intrinsic_matrix = get_intrinsic_opengl_params(f, f, height, width, zfar=zfar, znear=znear)

    homogeneous_points = convert_to_homogenous(points)
    camera_coordinates = homogeneous_points @ extrinsic_matrix.T
    clip_coordinates = camera_coordinates @ intrinsic_matrix.T 
    point_ids = cull_coordinates_ids(clip_coordinates, camera_coordinates, zfar=zfar, znear=znear) 

    ndc_coordinates = to_ndc_coordinates(clip_coordinates[point_ids])  
    selected_colors = colors[point_ids]
    screen_coordinates = to_screen_coordinates(ndc_coordinates, width, height, zfar, znear)

    return screen_coordinates, selected_colors, img

def show_projection(images_path, img, screen_coordinates, colors):
    image = mpimg.imread(images_path / f'{img.name}')
    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    plt.scatter(screen_coordinates[:, 0], screen_coordinates[:, 1], s=2, c=colors)
    plt.subplot(1, 2, 2)
    plt.imshow(image)
    plt.show()

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Project COLMAP reconstruction points onto an image.")
    
    parser.add_argument('--reconstruction_path', type=str, required=True, help='Path to the reconstruction files.')
    parser.add_argument('--images_path', type=str, required=True, help='Path to the folder of input images.')
    parser.add_argument('--img_id', type=int, required=True, help='Image ID for projection.')
    parser.add_argument('--cam_id', type=int, default=1, help='Camera ID (default is 1).')
    
    args = parser.parse_args()
    
    screen_coordinates, colors, img = project_image(args.reconstruction_path, args.img_id, args.cam_id)
    
    show_projection(Path(args.images_path), img, screen_coordinates, colors)