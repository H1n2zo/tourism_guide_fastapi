import os
import uuid
from datetime import datetime
from fastapi import UploadFile, HTTPException
from PIL import Image
from typing import Optional
from app.config import settings

ALLOWED_EXTENSIONS = settings.ALLOWED_EXTENSIONS
MAX_FILE_SIZE = settings.MAX_UPLOAD_SIZE

def validate_image(file: UploadFile) -> bool:
    """Validate image file"""
    # Check file extension
    ext = file.filename.split('.')[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    return True

def save_upload_file(file: UploadFile, subfolder: str = "destinations") -> str:
    """
    Save uploaded file and return relative path
    
    Args:
        file: UploadFile object
        subfolder: Subfolder name (destinations, categories, etc.)
    
    Returns:
        Relative path to saved file (e.g., "destinations/image.jpg")
    """
    validate_image(file)
    
    # Create directory if it doesn't exist
    upload_dir = os.path.join(settings.UPLOAD_DIR, subfolder)
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    ext = file.filename.split('.')[-1].lower()
    unique_filename = f"{uuid.uuid4().hex}_{int(datetime.now().timestamp())}.{ext}"
    file_path = os.path.join(upload_dir, unique_filename)
    
    # Save file
    try:
        contents = file.file.read()
        
        # Check file size
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size: {MAX_FILE_SIZE / (1024*1024)}MB"
            )
        
        with open(file_path, 'wb') as f:
            f.write(contents)
        
        # Verify it's a valid image
        try:
            img = Image.open(file_path)
            img.verify()
        except Exception:
            os.remove(file_path)
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Return relative path
        return os.path.join(subfolder, unique_filename).replace('\\', '/')
        
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    finally:
        file.file.close()

def delete_upload_file(file_path: str) -> bool:
    """Delete uploaded file"""
    try:
        full_path = os.path.join(settings.UPLOAD_DIR, file_path)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False
    except Exception:
        return False

def get_file_url(file_path: Optional[str]) -> Optional[str]:
    """Get full URL for file"""
    if not file_path:
        return None
    return f"/uploads/{file_path}"