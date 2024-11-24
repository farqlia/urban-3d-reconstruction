from src.urb3d.pipeline.config import INPUT_DATA_FOLDER, DATA_FOLDER, SCENE_FOLDER, GAUSSIAN_MODEL_PT, \
    GAUSSIAN_MODEL_PLY, GAUSSIAN_MODEL_SEG_PLY, COLMAP_ENV
from src.urb3d.pipeline.utils import run_script, run_script_with_env


class ModelProcessor:

    def __init__(self):
        self.input_folder = INPUT_DATA_FOLDER
        self.output_folder = DATA_FOLDER
        self.scene_folder = SCENE_FOLDER
        self.gaussian_pt_path = GAUSSIAN_MODEL_PT
        self.gaussian_ply_path = GAUSSIAN_MODEL_PLY

    def _reconstruct_point_cloud(self):
        if not self.output_folder.exists():
            run_script_with_env(COLMAP_ENV, "colmap_reconstruction.py", "--input", str(self.input_folder),
                 "--output", str(self.scene_folder))
        self.gaussian_ply_path = GAUSSIAN_MODEL_PLY

    def _create_gaussian_model(self): 
        if not self.gaussian_ply_path.exists():
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


    def _segment(self):
        print("_segment")
        self.gaussian_ply_path = GAUSSIAN_MODEL_SEG_PLY

    def run_full_reconstruction(self):
        self._reconstruct_point_cloud()
        self._create_gaussian_model()
