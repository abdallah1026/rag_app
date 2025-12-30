from .BaseControllers import BaseController
from models import ResponseSignals
from .ProjectControllers import ProjectController
import re

class DataController(BaseController):

    def __init__(self):
        super().__init__()
        self.SCALE_SIZE = 1024 * 1024    # convert to MB

    def validate_uploaded_file(self, file: UploadFile):
        
        if file.content_type not in self.app_settings.FILE_ALLOWED_EXTENSIONS:
            return False, ResponseSignals.FILE_VALIDATION_FAILED


        if file.size > self.app_settings.FILE_MAX_SIZE * self.SCALE_SIZE:
            return False, ResponseSignals.FILE_SIZE_EXCEEDED

        return True, ResponseSignals.FILE_VALIDATION_SUCCESS


    def generate_uniqe_file_name(self, file_name: str, project_id: str):

        randomfile_name = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)

        cleaned_file_name = self.get_clean_file_name(file_name=file_name)

        new_file_path = os.path.join(project_path, randomfile_name + "_" + cleaned_file_name)

        while os.path.exists(new_file_path):
            randomfile_name = self.generate_random_string()
            new_file_path = os.path.join(project_path, randomfile_name + "_" + cleaned_file_name)

        return new_file_path, randomfile_name + "_" + cleaned_file_name

    def get_clean_file_name(self, file_name: str):
        
        cleaned_file_name = re.sub(r'[^\W.]', '', file_name.strip())

        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name
        
        