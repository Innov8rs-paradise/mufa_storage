from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import Base, engine, get_db
import src.crud, src.schemas
from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import FileResponse, JSONResponse
import os
import shutil
import uuid
from typing import List
import zipfile
import tempfile



app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/users/", response_model=src.schemas.UserOut)
def create_user(user: src.schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = src.crud.get_user(db, user.id)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return src.crud.create_user(db, user)

@app.get("/users/{user_id}", response_model=src.schemas.UserOut)
def read_user(user_id: str, db: Session = Depends(get_db)):
    user = src.crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


app = FastAPI()

UPLOAD_DIR = "uploaded_photos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/photos/{user_id}")
async def upload_photos(user_id: str, files: List[UploadFile] = File(...)):
    saved_files = []
    user_dir = os.path.join(UPLOAD_DIR, user_id)
    os.makedirs(user_dir, exist_ok=True)

    for upload in files:
        ext = os.path.splitext(upload.filename)[1]
        filename = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(user_dir, filename)

        with open(file_path, "wb") as f:
            shutil.copyfileobj(upload.file, f)

        saved_files.append({"original_filename": upload.filename, "file_path": file_path})

    return JSONResponse(content={"uploaded": saved_files})

@app.get("/photos/{user_id}")
async def list_user_photos(user_id: str):
    user_dir = os.path.join(UPLOAD_DIR, user_id)
    if not os.path.exists(user_dir):
        return JSONResponse(status_code=404, content={"error": "User folder not found"})

    files = os.listdir(user_dir)
    photo_paths = [os.path.join(user_dir, fname) for fname in files]

    return JSONResponse(content={"photos": photo_paths})

@app.get("/photos/{user_id}/download")
async def download_user_photos(user_id: str, filename: str = Query(None)):
    user_dir = os.path.join(UPLOAD_DIR, user_id)

    if not os.path.exists(user_dir) or not os.listdir(user_dir):
        raise HTTPException(status_code=404, detail="No photos found for this user")

    # 🔹 If filename is provided, try to return that specific file
    if filename:
        file_path = os.path.join(user_dir, filename)
        if os.path.exists(file_path):
            return FileResponse(
                path=file_path,
                filename=filename,
                media_type="application/octet-stream"
            )
        else:
            raise HTTPException(status_code=404, detail="Requested file not found")

    # 🔹 Otherwise, zip and return all files
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, f"{user_id}_photos.zip")

    with zipfile.ZipFile(zip_path, "w") as zipf:
        for fname in os.listdir(user_dir):
            fpath = os.path.join(user_dir, fname)
            zipf.write(fpath, arcname=fname)

    return FileResponse(
        path=zip_path,
        filename=f"{user_id}_photos.zip",
        media_type="application/zip")