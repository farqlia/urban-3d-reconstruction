from src.urb3d.config import INPUT_DATA_FOLDER, DATA_FOLDER, SCENE_FOLDER, GAUSSIAN_MODEL_PT, \
    GAUSSIAN_MODEL_PLY, GAUSSIAN_MODEL_SEG_PLY, COLMAP_ENV, CHECKPOINT_DIR
from src.urb3d.pipeline.utils import run_script, run_script_with_env


class ModelProcessor:

    def __init__(self):
        self.input_folder = INPUT_DATA_FOLDER
        self.output_folder = DATA_FOLDER
        self.scene_folder = SCENE_FOLDER
        self.gaussian_pt_path = GAUSSIAN_MODEL_PT
        # How to pass to controller currently viewed cloud?
        self.gaussian_ply_path = GAUSSIAN_MODEL_PLY

    def _reconstruct_point_cloud(self):
        if not self.output_folder.exists():
            run_script_with_env(COLMAP_ENV, "colmap_reconstruction.py", "--input", str(self.input_folder),
                 "--output", str(self.scene_folder))

    def _create_gaussian_model(self): 
        if not GAUSSIAN_MODEL_PLY.exists():
            if not self.gaussian_pt_path.exists():
                # Add arguments to trainer
                run_script("simple_trainer.py", "--data_dir", str(self.output_folder),  #?
                           "--result_dir", str(self.scene_folder), "--max_steps", "100")
                run_script("ckpt_to_final_model.py", "--ckpts_dir", str(self.scene_folder / 'ckpts'))

            run_script("torch_model_to_ply.py", "--input", str(self.scene_folder / 'model.pt'),
                       "--output", str(self.scene_folder / 'model.ply'))

            run_script("add_rgb_color.py", "--input", str(self.scene_folder / 'model.ply'))

        run_script(r"gs_viewer.py", "--model_path",
                   self.gaussian_ply_path)

        self.gaussian_ply_path = GAUSSIAN_MODEL_PLY


    def _segment(self):
        if not GAUSSIAN_MODEL_SEG_PLY.exists():
            run_script("segmentation.py", "--ckpt", CHECKPOINT_DIR,
                       "--input", self.gaussian_ply_path, "--output", GAUSSIAN_MODEL_SEG_PLY)

        self.gaussian_ply_path = GAUSSIAN_MODEL_SEG_PLY

    def run_full_reconstruction(self):
        self._reconstruct_point_cloud()
        self._create_gaussian_model()
