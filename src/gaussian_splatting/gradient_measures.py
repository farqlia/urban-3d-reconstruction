import numpy as np
import torch
from matplotlib import pyplot as plt


class GradientMeasure:

    def __init__(self, points, rot, scale_exponents, color_exponents, alpha_exponents):
        self.points = points
        self.rot = rot
        self.scale_exponents = scale_exponents
        self.color_exponents = color_exponents
        self.alpha_exponents = alpha_exponents

        self.point_gradients = []
        self.rot_gradients = []
        self.scale_exp_gradients = []
        self.color_exp_gradients = []
        self.alpha_exp_gradients = []

    def add_pixel_gradient(self):
        self.point_gradients.append([])
        self.rot_gradients.append([])
        self.scale_exp_gradients.append([])
        self.color_exp_gradients.append([])
        self.alpha_exp_gradients.append([])

    def accumulate_pixel_gradient(self, splat_ids):
        self.point_gradients[-1].append(torch.sum(torch.abs(self.points.grad[splat_ids])).clone().cpu().detach().item())
        self.rot_gradients[-1].append(torch.sum(torch.abs(self.rot.grad[splat_ids])).clone().cpu().detach().item())
        self.scale_exp_gradients[-1].append(torch.sum(torch.abs(self.scale_exponents.grad[splat_ids])).clone().cpu().detach().item())
        self.color_exp_gradients[-1].append(torch.sum(torch.abs(self.color_exponents.grad[splat_ids])).clone().cpu().detach().item())
        self.alpha_exp_gradients[-1].append(torch.sum(torch.abs(self.alpha_exponents.grad[splat_ids])).clone().cpu().detach().item())

    def agg_gradient_stats(self):
        # maybe mean? avg? min-max??
        point_grads = [np.mean(grads) for grads in self.point_gradients]
        rot_grads = [np.mean(grads) for grads in self.rot_gradients]
        scale_exp_grads = [np.mean(grads) for grads in self.scale_exp_gradients]
        color_exp_grads = [np.mean(grads) for grads in self.color_exp_gradients]
        alpha_exp_grads = [np.mean(grads) for grads in self.alpha_exp_gradients]

        return point_grads, rot_grads, scale_exp_grads, color_exp_grads, alpha_exp_grads

    def plot_gradient_stats(self):
        point_grads, rot_grads, scale_exp_grads, color_exp_grads, alpha_exp_grads = self.agg_gradient_stats()

        plt.figure(figsize=(12, 8))
        plt.subplot(2, 3, 1)
        plt.title('Point grads')
        plt.hist(point_grads)
        plt.subplot(2, 3, 2)
        plt.title('Rot grads')
        plt.hist(rot_grads)
        plt.subplot(2, 3, 3)
        plt.title('Scale grads')
        plt.hist(scale_exp_grads)
        plt.subplot(2, 3, 4)
        plt.title('Color grads')
        plt.hist(color_exp_grads)
        plt.subplot(2, 3, 5)
        plt.title('Alpha grads')
        plt.hist(alpha_exp_grads)
        plt.show()