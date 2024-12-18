import torch
import torch.nn as nn
import torch.nn.functional as F
from urb3d.segmentation.tnet import Tnet

class Transform(nn.Module):
    def __init__(self):
        super().__init__()
        self.input_transform = Tnet(k=3)
        self.feature_transform = Tnet(k=64)
        self.conv1 = nn.Conv1d(3, 64, 1)
        self.conv2 = nn.Conv1d(64, 128, 1)
        self.conv3 = nn.Conv1d(128, 1024, 1)

        self.bn1 = nn.BatchNorm1d(64)
        self.bn2 = nn.BatchNorm1d(128)
        self.bn3 = nn.BatchNorm1d(1024)

    def forward(self, input):
        matrix3x3 = self.input_transform(input)
        # batch matrix multiplication
        xb = torch.bmm(torch.transpose(input, 1, 2), matrix3x3).transpose(1, 2)

        xb = F.relu(self.bn1(self.conv1(xb)))

        matrix64x64 = self.feature_transform(xb)
        xb = torch.bmm(torch.transpose(xb, 1, 2), matrix64x64).transpose(1, 2)

        # compute global features
        global_xb = F.relu(self.bn2(self.conv2(xb)))
        global_xb = self.bn3(self.conv3(global_xb))
        global_xb = nn.MaxPool1d(global_xb.size(-1))(global_xb).transpose(2, 1)  # global feature (bs, 1024, 1?)

        return xb, global_xb, matrix3x3, matrix64x64
