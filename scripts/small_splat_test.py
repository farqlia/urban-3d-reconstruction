import matplotlib.pyplot as plt
import numpy as np
import torch
from gsplat import rasterization
# Initialize a 3D Gaussian :
device = "cuda:0"
means = torch.randn((100, 3), device=device)
quats = torch.randn((100, 4), device=device)
scales = torch.rand((100, 3), device=device) * 0.25
colors = torch.rand((100, 3), device=device)
opacities = torch.rand((100,), device=device)
viewmats = torch.eye(4, device=device)[None, :, :]
Ks = torch.tensor([
   [300., 0., 150.], [0., 300., 100.], [0., 0., 1.]], device=device)[None, :, :]
width, height = 300, 200
colors, alphas, meta = rasterization(
   means, quats, scales, opacities, colors, viewmats, Ks, width, height
)
img_np = colors.cpu()[0].numpy()
print(np.mean(img_np))

plt.imshow(img_np)
plt.show()