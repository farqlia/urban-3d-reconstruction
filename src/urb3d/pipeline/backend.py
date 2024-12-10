from src.urb3d.pipeline.file_manager import FileManager
from src.urb3d.pipeline.model_processor import ModelProcessor
from src.urb3d.pipeline.segmentation_processor import SegmentationProcessor
from src.urb3d.pipeline.config import POINT_CLOUD_SPARSE, GAUSSIAN_MODEL_PLY, SEGMENTED_PLY_PATH
from PySide6.QtCore import QObject, Slot

PREFIX_LENGTH = 8
class Backend(QObject):

    def __init__(self):
        super().__init__()
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
        self.file_manager.save_result(to_save_path, destination_path[PREFIX_LENGTH:])

    @Slot(str)
    def save_cloud(self, destination_path):
        destination_file = destination_path + "/pcd.ply"
        self.save_result(POINT_CLOUD_SPARSE, destination_file)

    @Slot(str)
    def save_gaussian_model(self, destination_path):
        destination_file = destination_path + "/gaussian_model.ply"
        self.save_result(GAUSSIAN_MODEL_PLY, destination_file)

    @Slot(str)
    def save_segmented_model(self, destination_path):
        destination_file = destination_path + "/segmented_model.ply"
        self.save_result(SEGMENTED_PLY_PATH, destination_file)

    @Slot(str)
    def upload_reconstruction(self, src_path):
        self.file_manager.upload_reconstruction(src_path[PREFIX_LENGTH:])

    @Slot()
    def clear_reconstruction(self):
        self.file_manager.clear_reconstruction()

    @Slot(str)
    def upload_gaussian_ckpts(self, source_path):
        self.file_manager.upload_gaussian_ckpts(source_path[PREFIX_LENGTH:])

    @Slot()
    def clear_gaussian_model(self):
        self.file_manager.clear_gaussian_model()