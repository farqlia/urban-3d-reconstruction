import torch
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as pl
from torchmetrics import Precision, Accuracy, Recall
from urb3d.segmentation.transform import Transform

def segmentation_loss(outputs, labels, m3x3, m64x64, alpha=0.001, criterion=None):
    '''
    Cross entropy loss plus regularization for transformation matrices
    '''
    if criterion is None:
        criterion = torch.nn.CrossEntropyLoss()
    bs=outputs.size(0)
    id3x3 = torch.eye(3, requires_grad=True).repeat(bs,1,1)
    id64x64 = torch.eye(64, requires_grad=True).repeat(bs,1,1)
    if outputs.is_cuda:
        id3x3=id3x3.cuda()
        id64x64=id64x64.cuda()
    diff3x3 = id3x3-torch.bmm(m3x3,m3x3.transpose(1,2))
    diff64x64 = id64x64-torch.bmm(m64x64,m64x64.transpose(1,2))
    return criterion(outputs, labels) + alpha * (torch.norm(diff3x3)+torch.norm(diff64x64)) / float(bs)

class PointNetSegmentor(pl.LightningModule):
    def __init__(self, classes=13, weights=None):
        super().__init__()
        self.criterion = torch.nn.CrossEntropyLoss() if weights is None else torch.nn.CrossEntropyLoss(weight=weights)
        self.precision = Precision(task="multiclass", average='macro', num_classes=classes)
        self.recall = Recall(task="multiclass", average='macro', num_classes=classes)
        self.accuracy = Accuracy(task="multiclass", num_classes=classes)
        self.transform = Transform()
        self.conv1 = nn.Conv1d(1088, 512, 1)
        self.conv2 = nn.Conv1d(512, 256, 1)
        self.conv3 = nn.Conv1d(256, 128, 1)
        self.conv4 = nn.Conv1d(128, classes, 1)

        self.bn1 = nn.BatchNorm1d(512)
        self.bn2 = nn.BatchNorm1d(256)
        self.bn3 = nn.BatchNorm1d(128)
        self.bn4 = nn.BatchNorm1d(classes)

        self.dropout = nn.Dropout(p=0.3)

    def forward(self, input):
        xb, g_x, matrix3x3, matrix64x64 = self.transform(input)  # xb is of shape (bs, 63, cld_s)
        cld_s = xb.shape[-1]

        g = torch.repeat_interleave(g_x, cld_s, dim=1)
        x = torch.concat([xb.transpose(1, 2), g], dim=2).transpose(1, 2)  # concatenate global and per-point features

        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))
        x = F.relu(self.dropout(self.bn4(self.conv4(x))))

        return x, matrix3x3, matrix64x64

    def training_step(self, batch, batch_idx):
        x, y = batch
        predictions, matrix3x3, matrix64x64 = self(x)
        loss = segmentation_loss(predictions, y, matrix3x3, matrix64x64, criterion=self.criterion)
        self.log('train_loss', loss, prog_bar=True, sync_dist=True, on_epoch=True)
        self.log('train_accuracy', self.accuracy(predictions, y), prog_bar=True, sync_dist=True, on_epoch=True)
        self.log('train_precision', self.precision(predictions, y), prog_bar=True, sync_dist=True, on_epoch=True)
        self.log('train_recall', self.recall(predictions, y), prog_bar=True, sync_dist=True, on_epoch=True)
        return {'loss': loss}

    def validation_step(self, batch, batch_idx):
        x, y = batch
        predictions, matrix3x3, matrix64x64 = self(x)
        loss = segmentation_loss(predictions, y, matrix3x3, matrix64x64, criterion=self.criterion)
        self.log('val_loss', loss, prog_bar=True, sync_dist=True, on_epoch=True)
        self.log('val_accuracy', self.accuracy(predictions, y), prog_bar=True, sync_dist=True, on_epoch=True)
        self.log('val_precision', self.precision(predictions, y), prog_bar=True, sync_dist=True, on_epoch=True)
        self.log('val_recall', self.recall(predictions, y), prog_bar=True, sync_dist=True, on_epoch=True)
        return {'val_loss': loss}

    def predict_step(self, batch, batch_idx, dataloader_idx=0):
        predictions, _, _ = self(batch)
        return torch.argmax(predictions, dim=1)

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        return optimizer