import torch
import numpy as np
import pyntcloud
import pandas as pd

def convert(model_path, output_path):
    model = torch.load(model_path, map_location="cpu", weights_only=True)
    N = model['splats']['shN'].shape[1]
    shN_cols = np.array([[f'sh{i}_x', f'sh{i}_y', f'sh{i}_z'] for i in range(1, N + 1)]).flatten()
    shN = model['splats']['shN'].reshape(len(model['splats']['means']), -1)
    columns = np.array(['x', 'y', 'z', 'a', 'q0', 'q1', 'q2', 'q3', 's0', 's1', 's2', 'sh0_x', 'sh0_y', 'sh0_z'])
    columns = np.concatenate((columns, shN_cols))

    data = np.column_stack((model['splats']['means'].numpy(),
                            model['splats']['opacities'].numpy(),
                            model['splats']['quats'].numpy(),
                            model['splats']['scales'].numpy(),
                            model['splats']['sh0'].reshape(-1, 3),
                            shN))

    pd_data = pd.DataFrame(data, columns=columns)
    cloud = pyntcloud.PyntCloud(pd_data)
    cloud.points['z'] = cloud.points['z'] * -1
    # cloud.points['y'] = cloud.points['y'] * -1
    cloud.to_file(output_path)