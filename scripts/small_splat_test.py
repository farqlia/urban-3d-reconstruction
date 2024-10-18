import torch
from gsplat import rasterization
# Initialize a 3D Gaussian :
mean = torch.tensor([[0.0, 0.0, 0.0]], device="cuda:0")
quat = torch.tensor([[1.0, 0.0, 0.0, 0.0]], device="cuda:0")
color = torch.rand((1, 3), device="cuda:0")
opac = torch.ones((1,), device="cuda:0")
scale = torch.rand((1, 3), device="cuda:0")
view = torch.eye(4, device="cuda:0")[None]
K = torch.tensor([[[1.0, 0.0, 120.], [0., 1., 120.], [0., 0., 1.]]], device="cuda:0")
rgb_image, alpha, metadata = rasterization(
    mean, quat, color, opac, scale, view, K, 240, 240
)