import shutil
from pathlib import Path
from tqdm import tqdm
from config import INPUT_DATA_FOLDER

class FileManager:
    def __init__(self):
        self.destination_folder = INPUT_DATA_FOLDER
        self.destination_folder.mkdir(parents=True, exist_ok=True)

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
