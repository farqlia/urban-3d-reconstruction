import pycolmap
recon_id = 1

input_dir = f"../data/small_city_road_outside-d2x/sparse/{recon_id}"
input_images_path = "../data/small_city_road_outside-d2x/images"
output_dir = f"../data/small_city_road_outside-d2x/sparse/undistorted_images_{recon_id}"

pycolmap.undistort_images(output_path=output_dir,
                                  image_path=input_images_path, input_path=input_dir)

