import torch
import open3d as o3d
import matplotlib.pyplot as plt
import numpy as np

g_model = torch.load("../results/small_city_road_down_test/epochs_200_000/ckpts/ckpt_199999_rank0.pt", map_location="cpu", weights_only=True)

gs_cloud = o3d.geometry.PointCloud()
gs_cloud.points = o3d.utility.Vector3dVector(g_model['splats']['means'].numpy()[:10])