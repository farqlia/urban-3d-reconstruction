import os
import shutil
from pathlib import Path


def remove_ckpts(ckpt_path):
    ckpts = os.listdir(ckpt_path)
    assert str(ckpt_path).endswith("ckpts")
    iter_to_ckpt = {
        int(name.split("_")[1]): name for name in ckpts
    }
    final_model = iter_to_ckpt[max(iter_to_ckpt.keys())]
    shutil.copy(ckpt_path / final_model, ckpt_path.parent / 'model.pt')
    print(f"...Saving model {final_model}")
    shutil.rmtree(ckpt_path)


if __name__ == '__main__':
    remove_ckpts(Path("../../results/south-building/epochs_30_000/ckpts"))
