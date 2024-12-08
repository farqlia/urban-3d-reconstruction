from src.urb3d.pipeline.file_manager import FileManager
from src.urb3d.pipeline.model_processor import ModelProcessor
from src.urb3d.pipeline.segmentation_processor import SegmentationProcessor

class Backend:

    def __init__(self):
        self.model_processor = ModelProcessor()
        self.segmentation_processor = SegmentationProcessor()
        self.file_manager = FileManager()

    def reconstruct_point_cloud(self):
        self.model_processor._reconstruct_point_cloud()

    def create_gaussian_model(self, strategy : str = "default", max_steps : int = 1_000, cap_max : int = 3_000_000,
                              refine_every : int = 100, sh_degree : int = 3):
        self.model_processor._create_gaussian_model(strategy=strategy, max_steps=max_steps, cap_max=cap_max, refine_every=refine_every,
                                                    sh_degree=sh_degree)

    def run_segmentation(self):
        self.segmentation_processor.run_segmentation()

    def upload_image_folder(self, source_folder):
        self.file_manager.upload_folder(source_folder)

    def save_result(self, to_save_path, destination_path):
        self.file_manager.save_result(to_save_path, destination_path)

    def upload_gaussian_model(self, source_path):
        self.file_manager.upload_gaussian_model(source_path)