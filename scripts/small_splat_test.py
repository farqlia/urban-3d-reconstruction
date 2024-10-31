import pandas as pd
import torch
import numpy as np
import pyntcloud

g_model = torch.load("../results/south-building/ckpts/ckpt_6999_rank0.pt", map_location="cpu", weights_only=True)