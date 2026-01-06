from fastapi import FastAPI, APIRouter, Depends, UploadFile, status,Request
from fastapi.responses import JSONResponse
import os
from ..models.enums.signalsResponse import ResponseSignals
from ..helper.config import get_settings, Settings
from ..controllers import DataController, ProjectController
import aiofiles
from .schemes.data import ProcessRequest
import logging
from ..controllers import ProcessController
from ..models.project_model import ProjectModel

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter()


@data_router.post("/upload/{project_id}")
async def upload_data(request: Request ,project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):

    project_model = ProjectModel(
        db_client=request.app.db_client,
    )

    project =await project_model.get_project_or_create_one(project_id=project_id)

    IsValid, status = DataController().validate_uploaded_file(file=file)

    if not IsValid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, 
            content=
            {"message": status
            }
        )
    
    data_controller = DataController()

    project_dir = data_controller.get_project_path(project_id=project_id)

    file_path, file_id = data_controller.generate_uniqe_file_name(file_name=file.filename, project_id=project_id)


    file_path = os.path.join(project_dir, file.filename)
    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFUALTE_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:

        logger.error(f"Error uploading file: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content=
            {
                "message": ResponseSignals.FILE_UPLOAD_FAILED.value

            }
        )


    return JSONResponse( 
        content=
        {"message": ResponseSignals.FILE_UPLOAD_SUCCESS.value,
        "file_id": file_id,
        }
    )


@data_router.post("/process/{project_id}")
async def process_data(project_id: str, process_request: ProcessRequest):

    file_id = process_request.file_id


    process_controller = ProcessController(project_id=project_id)

    file_content = process_controller.get_file_content(file_id=file_id)

    file_chunks = process_controller.process_file_content(
        content_file=file_content,
        chunk_size=process_request.chunk_size,
        overlap_size=process_request.overlap_size,
        file_id=file_id
    )

    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, 
            content=
            {
                "message": ResponseSignals.FILE_PROCESS_FAILED.value
            }
        )

    return file_chunks


    
