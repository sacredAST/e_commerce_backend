from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
import os
import uuid

router = APIRouter()

UPLOAD_DIRECTORY = "./uploads"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    uuid_name = uuid.uuid4()
    file_path = os.path.join(UPLOAD_DIRECTORY, f"{uuid_name}_{file.filename}")
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    return JSONResponse({"filepath": f"uploads/{uuid_name}_{file.filename}", "message": "File uploaded successfully."})
