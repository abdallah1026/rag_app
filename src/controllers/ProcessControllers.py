from .BaseControllers import BaseController
from ProjectControllers import ProjectController
from models import ProcessingEnum
import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter



class ProcessController(BaseController):
    
    def __init__(self, project_id: str):
        super().__init__()

        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    def get_file_extension(self, file_id: str):
        os.path.splitext(file_id)[-1]
    

    def get_file_loader(self, file_id: str):
        
        file_extension = self.get_file_extension(file_id=file_id)
        
        if file_extension == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(os.path.join(self.project_path, file_id), )
        elif file_extension == ProcessingEnum.TXT.value:
            return TextLoader(os.path.join(self.project_path, file_id), encoding="utf-8")

        return None
    
    def get_file_content(self, file_id: str):

        loader = self.get_file_loader(file_id=file_id)
        
        return loader.load()    

    def process_file_content(self, file_id: str, chunk_size: int=100, overlap_size: int=20, content_file: List):

        text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=overlap_size,
        length_function=len,
        
        )

        file_content_text = [
            rec.page_content
            for rec in file_content:
        ]
        
        file_content_metadata = [
            rec.metadata
            for rec in file_content
        ]


        chunks = text_splitter.create_documents(
            file_content_text,
            metadatas=file_content_metadata
        )

        return chunks