import os
import shutil


def save_ckpt(ckpts_path) -> int:
    '''
    Saves the model from the last checkpoint
    :param ckpts_path: path to the checkpoint directories
    :return iteration at which the checkpoint was saved
    '''
    ckpts = os.listdir(ckpts_path)
    assert str(ckpts_path).endswith("ckpts")
    iter_to_ckpt = {
        int(name.split("_")[1]): name for name in ckpts
    }
    final_model = iter_to_ckpt[max(iter_to_ckpt.keys())]
    shutil.copy(ckpts_path / final_model, ckpts_path.parent / 'model.pt')
    print(f"...Saving model {final_model}")
    return max(iter_to_ckpt.keys())