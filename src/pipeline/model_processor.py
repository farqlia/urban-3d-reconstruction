from src.pipeline.config import INPUT_DATA_FOLDER, DATA_FOLDER, COLMAP_RECONSTRUCTION_DIR, GAUSSIAN_MODEL_PT, GAUSSIAN_MODEL_PLY, GAUSSIAN_MODEL_SEG_PLY
from src.pipeline.utils import run_script

class ModelProcessor:

    def __init__(self):
        self.input_folder = INPUT_DATA_FOLDER
        self.output_folder = DATA_FOLDER
        self.output_folder.mkdir(parents=True, exist_ok=True)
        self.reconstruction_folder = COLMAP_RECONSTRUCTION_DIR
        self.gaussian_pt_path = GAUSSIAN_MODEL_PT
        self.gaussian_ply_path = GAUSSIAN_MODEL_PLY

    def _reconstruct_point_cloud(self):
        if not self.reconstruction_folder.exists():
            run_script("colmap_reconstruction.py", "--input", str(self.input_folder),
                 "--output", str(self.output_folder))
        self.gaussian_ply_path = GAUSSIAN_MODEL_PLY

    def _create_gaussian_model(self): 
        if not self.gaussian_ply_path.exists():
            if not self.gaussian_pt_path.exists():
                # Add arguments to trainer
                run_script("simple_trainer.py", "--data_dir", str(self.output_folder),  #?
                           "--result_dir", str(self.output_folder), "--max_steps", "100")
                run_script("ckpt_to_final_model.py", "--ckpts_dir", str(self.output_folder / 'ckpts'))

            run_script("torch_model_to_ply.py", "--input", str(self.output_folder / 'model.pt'),
                       "--output", str(self.output_folder / 'model.ply'))

            run_script("add_rgb_color.py", "--input", str(self.output_folder / 'model.ply'))

        run_script(r"gs_viewer.py", "--model_path",
                   self.gaussian_ply_path)


    def _segment(self):
        print("_segment")

        self.gaussian_ply_path = GAUSSIAN_MODEL_SEG_PLY

    def run_full_reconstruction(self):
        self._reconstruct_point_cloud()
        self._create_gaussian_model()
