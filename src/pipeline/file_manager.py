from dotenv import load_dotenv
import os
import shutil
from pathlib import Path
from typing import List
from tqdm import tqdm

BASE_DIR = Path(__file__).resolve().parents[2]

class FileManager:
    def __init__(self):
        load_dotenv()
        self.destination_folder = BASE_DIR / os.getenv("INPUT_DATA_FOLDER")
        #self.destination_folder = Path(input_path)
        self.destination_folder.mkdir(parents=True, exist_ok=True)

    def upload_folder(self, source_folder: str) -> None:
        """Copies all images from the source folder to the destination folder."""
        source_path = Path(source_folder)
        if not source_path.exists() or not source_path.is_dir():
            raise FileNotFoundError(f"Source folder '{source_folder}' does not exist or is not a directory.")
        
        img_files = [f for f in source_path.glob("*") if f.is_file()]

        # Copy each file with a progress bar
        for img_file in tqdm(img_files, desc="Copying images", unit="file"):
            shutil.copy(img_file, self.destination_folder)

    def delete_image(self, image_name: str) -> None:
        """Deletes an image from the destination folder."""
        image_path = self.destination_folder / image_name
        if image_path.exists():
            image_path.unlink()
        else:
            raise FileNotFoundError(f"Image '{image_name}' does not exist in the destination folder.")

    def add_image(self, image_path: str) -> None:
        """Adds a single image to the destination folder."""
        image_file = Path(image_path)
        if image_file.exists() and image_file.is_file():
            shutil.copy(image_file, self.destination_folder)
        else:
            raise FileNotFoundError(f"Image '{image_path}' does not exist.")

    def list_images(self) -> List[str]:
        """Returns a list of all image filenames in the destination folder."""
        return [file.name for file in self.destination_folder.glob("*") if file.is_file()]


if __name__=="__main__":
    fm = FileManager()
    