import subprocess
from config import INPUT_DATA_FOLDER, DATA_FOLDER, SCRIPTS_DIR, COLMAP_RECONSTRUCTION_DIR

class ModelProcessor():

    def __init__(self):
        self.input_folder = INPUT_DATA_FOLDER
        self.output_folder = DATA_FOLDER
        self.output_folder.mkdir(parents=True, exist_ok=True)
        self.reconstruction_folder = COLMAP_RECONSTRUCTION_DIR

    def _reconstruct_point_cloud(self):
        subprocess.run(["python", SCRIPTS_DIR / "colmap_reconstruction.py", "--input", self.input_folder, 
                        "--output", self.output_folder])

    def _create_gaussian_model(self):
        subprocess.run(["python", SCRIPTS_DIR / "simple_trainer.py", "--data_dir", self.reconstruction_folder,
                        "--result_dir", self.output_folder]) #?
        

    def run_full_reconstruction(self):
        self._reconstruct_point_cloud()
        self._create_gaussian_model()
