import shutil
from pathlib import Path
from tqdm import tqdm
from urb3d.pipeline.config import INPUT_DATA_FOLDER, GAUSSIAN_MODEL_PLY, COLMAP_RECONSTRUCTION_DIR, GAUSSIAN_MODEL_PT, CKPTS_PATH, PNG_RENDERS_FOLDER

class FileManager:
    def __init__(self):
        self.destination_folder = INPUT_DATA_FOLDER
        self.model_pt_path = GAUSSIAN_MODEL_PT
        self.model_ply_path = GAUSSIAN_MODEL_PLY
        self.destination_folder.mkdir(parents=True, exist_ok=True)
        self.reconstruction_dir = COLMAP_RECONSTRUCTION_DIR
        self.ckpts_path = CKPTS_PATH
        self.renders_dir = PNG_RENDERS_FOLDER

    def upload_folder(self, source_folder: str) -> None:
        source_path = Path(source_folder)
        if not source_path.exists() or not source_path.is_dir():
            raise FileNotFoundError(f"Source folder '{source_folder}' does not exist or is not a directory.")
        
        img_files = [f for f in source_path.glob("*") if f.is_file()]

        for img_file in tqdm(img_files, desc="Copying images", unit="file"):
            shutil.copy(img_file, self.destination_folder)

    def delete_image(self, image_name: str) -> None:
        image_path = self.destination_folder / image_name
        if image_path.exists():
            image_path.unlink()
        else:
            raise FileNotFoundError(f"Image '{image_name}' does not exist in the destination folder.")

    def add_image(self, image_path: str) -> None:
        image_file = Path(image_path)
        if image_file.exists() and image_file.is_file():
            shutil.copy(image_file, self.destination_folder)
        else:
            raise FileNotFoundError(f"Image '{image_path}' does not exist.")
        
    def save_model(self, destination_path: str) -> None:
        destination_file = Path(destination_path)
        
        if not self.model_path.exists() or not self.model_path.is_file():
            raise FileNotFoundError(f"Model file '{self.model_path}' does not exist.")
        
        shutil.copy(self.model_path, destination_file)

    def save_result(self, to_save_path, destination_path):
        destination_file = Path(destination_path)
        if not to_save_path.exists() or not to_save_path.is_file():
            raise FileNotFoundError(f"Model file '{to_save_path}' does not exist.")
        shutil.copy(to_save_path, destination_file)

    def upload_reconstruction(self, src_path):
        src_path = Path(src_path)

        if not src_path.is_dir():
            raise FileNotFoundError(f"Path does not exist or is not a directory: {src_path}")

        required_folders = ["sparse", "images"]
        missing_folders = [folder for folder in required_folders if not (src_path / folder).is_dir()]
        if missing_folders:
            raise FileNotFoundError(f"Missing required folders: {', '.join(missing_folders)}")

        sparse_folder = src_path / "sparse"
        required_files = ["cameras.bin", "images.bin", "points3D.bin"]
        missing_files = [file for file in required_files if not (sparse_folder / file).exists()]
        if missing_files:
            raise FileNotFoundError(f"Missing files in sparse folder: {', '.join(missing_files)}")

        if self.reconstruction_dir.exists():
            shutil.rmtree(self.reconstruction_dir)

        shutil.copytree(src_path, self.reconstruction_dir)


    def clear_reconstruction(self):
        if self.reconstruction_dir.exists():
            shutil.rmtree(self.reconstruction_dir)

    def upload_gaussian_ckpts(self, src_path):
        src_path = Path(src_path)

        if not src_path.is_dir():
            raise FileNotFoundError(f"Source path is not a valid directory: {src_path}")

        pt_files = list(src_path.glob("*.pt"))
        if not pt_files:
            raise FileNotFoundError(f"No .pt files found in the directory: {src_path}")

        self.ckpts_path.mkdir(parents=True, exist_ok=True)

        for existing_file in self.ckpts_path.iterdir():
            if existing_file.is_file():
                existing_file.unlink()

        for pt_file in pt_files:
            shutil.copy(pt_file, self.ckpts_path)

    def clear_gaussian_model(self):
        if self.model_ply_path.exists():
            self.model_ply_path.unlink()
        if self.model_pt_path.exists():
            self.model_pt_path.unlink()
        if self.ckpts_path.exists():
            shutil.rmtree(self.ckpts_path)
        if self.renders_dir.exists():
            shutil.rmtree(self.renders_dir)
