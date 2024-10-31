import os
import shutil
from pathlib import Path


def remove_ckpts(ckpt_path) -> int:
    '''
    Saves the model from the last checkpoint and removes all other checkpoints
    :param ckpt_path: path to checkpoint directories
    :return iteration at which the checkpoint was saved
    '''
    ckpts = os.listdir(ckpt_path)
    assert str(ckpt_path).endswith("ckpts")
    iter_to_ckpt = {
        int(name.split("_")[1]): name for name in ckpts
    }
    final_model = iter_to_ckpt[max(iter_to_ckpt.keys())]
    shutil.copy(ckpt_path / final_model, ckpt_path.parent / 'model.pt')
    print(f"...Saving model {final_model}")
    shutil.rmtree(ckpt_path)
    return max(iter_to_ckpt.keys())



if __name__ == '__main__':
    remove_ckpts(Path("../../results/south-building/epochs_30_000/ckpts"))
