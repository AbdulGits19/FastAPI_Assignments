from fastapi import HTTPException, UploadFile

# REQUIREMENT: Validate file type & size
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {"image/jpeg", "image/png", "application/pdf"}

def validate_file(file: UploadFile):
    # 1. Check File Size
    # Note: This requires seeking the end of the file to check size
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0) # Reset to beginning

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Max limit is 5MB.")

    # 2. Check File Type
    if file.content_type not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG, PNG, and PDF allowed.")
    
    return True