//Prerequisites: pip install fastapi uvicorn boto3 python-multipart

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import boto3
import os
import uuid

app = FastAPI(title="Physics AI Skeleton")

# CORS is vital for React to talk to Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Your React App
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# S3 Setup (Replace with your AWS keys or MinIO config)
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    region_name="us-east-1"
)
BUCKET_NAME = "physics-ai-mvp-bronze"

@app.get("/")
def health_check():
    return {"status": "System Online", "module": "Skeleton-v1"}

@app.post("/upload/geometry")
async def upload_geometry(file: UploadFile = File(...)):
    """
    1. Receives CAD file.
    2. Generates unique ID.
    3. Uploads to S3 Bronze Layer.
    """
    file_ext = file.filename.split(".")[-1]
    if file_ext not in ["stl", "obj", "step"]:
        raise HTTPException(status_code=400, detail="Unsupported file format")
    
    # Generate unique simulation ID
    sim_id = str(uuid.uuid4())
    s3_key = f"uploads/{sim_id}/{file.filename}"
    
    try:
        # Upload to S3
        s3_client.upload_fileobj(file.file, BUCKET_NAME, s3_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    return {
        "message": "Upload Successful", 
        "sim_id": sim_id, 
        "s3_path": s3_key
    }
