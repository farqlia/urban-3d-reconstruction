from .config import INPUT_DATA_FOLDER, DATA_FOLDER, COLMAP_RECONSTRUCTION_DIR, CKPTS_PATH, GAUSSIAN_MODEL_PLY, GAUSSIAN_MODEL_PT, COLMAP_ENV, POINT_CLOUD_SPARSE
from .utils import run_script, run_script_with_env

class ModelProcessor:

    def __init__(self):
        self.input_folder = INPUT_DATA_FOLDER
        self.output_folder = DATA_FOLDER
        self.reconstruction_folder = COLMAP_RECONSTRUCTION_DIR
        self.point_cloud_sparse = POINT_CLOUD_SPARSE
        self.ckpts_path = CKPTS_PATH
        self.gaussian_ply_path = GAUSSIAN_MODEL_PLY

    def _reconstruct_point_cloud(self):
        if not self.reconstruction_folder.exists():
            print("Colmap reconstruction running ...")
            run_script_with_env(COLMAP_ENV, "colmap_reconstruction.py", "--input", str(self.input_folder),
                       "--output", str(self.reconstruction_folder))
            self._remove_noises_sparse_reconstruction()
        if not self.point_cloud_sparse.exists():
            run_script_with_env(COLMAP_ENV, "convert_to_ply.py", "--point_cloud", str(self.point_cloud_sparse),
                                "--reconstruction_dir", str(self.reconstruction_folder))

    def _create_gaussian_model(self, strategy : str, max_steps : int, cap_max : int,
                              refine_every : int, sh_degree : int):
        if not self.gaussian_ply_path.exists():
            if not self.ckpts_path.exists():
                run_script("simple_trainer.py", "--data_dir", str(self.output_folder),
                           "--result_dir", str(self.output_folder), "--strategy", strategy, "--max_steps", str(max_steps),
                           "--cap_max", str(cap_max), "--refine_every", str(refine_every), "--sh_degree", str(sh_degree))

            run_script("save_model.py", "--ckpts", str(self.ckpts_path),
                       "--output", str(GAUSSIAN_MODEL_PLY))

            run_script("simple_trainer.py", "--data_dir", str(self.output_folder),  # ?
                       "--result_dir", str(self.output_folder), "--ckpt", GAUSSIAN_MODEL_PT)

            run_script("add_rgb_color.py", "--input", str(GAUSSIAN_MODEL_PLY))

    def _remove_noises_sparse_reconstruction(self):
        run_script_with_env(COLMAP_ENV, "neighbor-based_pcd_filtering.py", "--reconstruction_dir",
                            str(self.reconstruction_folder), "--point_cloud", str(self.point_cloud_sparse), "--method", "statistical")

    def _remove_noises_gaussian_model(self):
        pass
        
    def run_full_reconstruction(self):
        self._reconstruct_point_cloud()
        self._create_gaussian_model()
