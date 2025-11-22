"""
Utility Functions for Tourism Guide FastAPI
File uploads, image processing, helpers
"""

from fastapi import UploadFile, HTTPException, status
from PIL import Image
import os
import shutil
from pathlib import Path
from typing import Optional
import uuid
from datetime import datetime

from config.settings import settings


def get_upload_path(subfolder: str = "") -> Path:
    """Get upload directory path"""
    path = Path(settings.UPLOAD_DIR) / subfolder
    path.mkdir(parents=True, exist_ok=True)
    return path


def generate_unique_filename(original_filename: str) -> str:
    """Generate unique filename with timestamp and UUID"""
    ext = Path(original_filename).suffix.lower()
    unique_id = uuid.uuid4().hex[:8]
    timestamp = int(datetime.now().timestamp())
    return f"{unique_id}_{timestamp}{ext}"


def validate_file_extension(filename: str) -> bool:
    """Validate if file extension is allowed"""
    ext = Path(filename).suffix.lower().replace('.', '')
    return ext in settings.ALLOWED_EXTENSIONS


def validate_file_size(file_size: int) -> bool:
    """Validate if file size is within limit"""
    return file_size <= settings.MAX_UPLOAD_SIZE


async def save_upload_file(
    upload_file: UploadFile,
    subfolder: str = "destinations"
) -> str:
    """
    Save uploaded file and return relative path
    
    Args:
        upload_file: FastAPI UploadFile object
        subfolder: Subfolder within uploads directory
    
    Returns:
        Relative path to saved file (e.g., "destinations/abc123.jpg")
    
    Raises:
        HTTPException: If file validation fails
    """
    # Validate extension
    if not validate_file_extension(upload_file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    # Read file content
    content = await upload_file.read()
    file_size = len(content)
    
    # Validate size
    if not validate_file_size(file_size):
        max_mb = settings.MAX_UPLOAD_SIZE / (1024 * 1024)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size: {max_mb}MB"
        )
    
    # Validate it's actually an image
    try:
        image = Image.open(upload_file.file)
        image.verify()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file"
        )
    
    # Reset file pointer
    await upload_file.seek(0)
    
    # Generate unique filename
    new_filename = generate_unique_filename(upload_file.filename)
    
    # Get upload directory
    upload_dir = get_upload_path(subfolder)
    file_path = upload_dir / new_filename
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )
    
    # Return relative path
    return f"{subfolder}/{new_filename}"


def delete_upload_file(relative_path: str) -> bool:
    """
    Delete uploaded file
    
    Args:
        relative_path: Relative path to file (e.g., "destinations/abc123.jpg")
    
    Returns:
        True if deleted successfully, False otherwise
    """
    if not relative_path:
        return False
    
    file_path = Path(settings.UPLOAD_DIR) / relative_path
    
    try:
        if file_path.exists() and file_path.is_file():
            file_path.unlink()
            return True
    except Exception as e:
        print(f"Error deleting file {relative_path}: {e}")
    
    return False


def resize_image(
    image_path: Path,
    max_width: int = 1200,
    max_height: int = 800,
    quality: int = 85
) -> bool:
    """
    Resize image to fit within max dimensions while maintaining aspect ratio
    
    Args:
        image_path: Path to image file
        max_width: Maximum width in pixels
        max_height: Maximum height in pixels
        quality: JPEG quality (1-100)
    
    Returns:
        True if resized successfully, False otherwise
    """
    try:
        with Image.open(image_path) as img:
            # Convert RGBA to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Calculate new dimensions
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Save optimized image
            img.save(image_path, 'JPEG', quality=quality, optimize=True)
            
        return True
    except Exception as e:
        print(f"Error resizing image {image_path}: {e}")
        return False


def create_thumbnail(
    source_path: Path,
    thumbnail_size: tuple = (300, 300)
) -> Optional[Path]:
    """
    Create thumbnail for image
    
    Args:
        source_path: Path to source image
        thumbnail_size: Tuple of (width, height)
    
    Returns:
        Path to thumbnail or None if failed
    """
    try:
        thumb_path = source_path.parent / f"thumb_{source_path.name}"
        
        with Image.open(source_path) as img:
            # Convert RGBA to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            img.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
            img.save(thumb_path, 'JPEG', quality=80, optimize=True)
        
        return thumb_path
    except Exception as e:
        print(f"Error creating thumbnail: {e}")
        return None


def sanitize_filename(filename: str) -> str:
    """Remove unsafe characters from filename"""
    # Remove path separators and other unsafe characters
    unsafe_chars = ['/', '\\', '..', '<', '>', ':', '"', '|', '?', '*']
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    return filename


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two coordinates using Haversine formula
    
    Args:
        lat1, lon1: First coordinate
        lat2, lon2: Second coordinate
    
    Returns:
        Distance in kilometers
    """
    from math import radians, sin, cos, sqrt, atan2
    
    R = 6371  # Earth's radius in kilometers
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    distance = R * c
    return round(distance, 2)


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug"""
    import re
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)].rstrip() + suffix


def parse_coordinates(coord_string: str) -> Optional[tuple]:
    """
    Parse coordinate string to (latitude, longitude) tuple
    
    Examples:
        "11.0059, 124.6075" -> (11.0059, 124.6075)
        "11.0059,124.6075" -> (11.0059, 124.6075)
    """
    try:
        parts = coord_string.replace(' ', '').split(',')
        if len(parts) == 2:
            lat = float(parts[0])
            lng = float(parts[1])
            if -90 <= lat <= 90 and -180 <= lng <= 180:
                return (lat, lng)
    except (ValueError, IndexError):
        pass
    return None


def get_file_info(file_path: Path) -> dict:
    """Get file information"""
    if not file_path.exists():
        return None
    
    stat = file_path.stat()
    
    return {
        "name": file_path.name,
        "size": stat.st_size,
        "size_formatted": format_file_size(stat.st_size),
        "created": datetime.fromtimestamp(stat.st_ctime),
        "modified": datetime.fromtimestamp(stat.st_mtime),
        "extension": file_path.suffix.lower()
    }