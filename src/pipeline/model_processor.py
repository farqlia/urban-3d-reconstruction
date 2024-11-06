from config import INPUT_DATA_FOLDER, DATA_FOLDER, COLMAP_RECONSTRUCTION_DIR, CKPTS_PATH, GAUSSIAN_MODEL_PLY
from utils import run_script

class ModelProcessor():

    def __init__(self):
        self.input_folder = INPUT_DATA_FOLDER
        self.output_folder = DATA_FOLDER
        self.output_folder.mkdir(parents=True, exist_ok=True)
        self.reconstruction_folder = COLMAP_RECONSTRUCTION_DIR
        self.ckpts_path = CKPTS_PATH
        self.gaussian_ply_path = GAUSSIAN_MODEL_PLY

    def _reconstruct_point_cloud(self):
        if not self.reconstruction_folder.exists():
            run_script("colmap_reconstruction.py", "--input", str(self.input_folder),
                       "--output", str(self.output_folder))

    def _create_gaussian_model(self): 
        if not self.gaussian_ply_path.exists():
            if not self.ckpts_path.exists():
                run_script("simple_trainer.py", "--data_dir", str(self.reconstruction_folder),  #?
                           "--result_dir", str(self.output_folder))        
                
            run_script("save_model.py", "--ckpts", str(self.ckpts_path),
                       "--output", str(self.gaussian_ply_path))
        
    def run_full_reconstruction(self):
        self._reconstruct_point_cloud()
        self._create_gaussian_model()
