from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class FileType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"

class UploadRequest(BaseModel):
    subject: str = Field(..., description="Materia o asignatura relacionada con el documento")
    
    class Config:
        schema_extra = {
            "example": {
                "subject": "Matemáticas"
            }
        }

class UploadResponse(BaseModel):
    message: str
    file_name: Optional[str] = None
    file_type: Optional[str] = None
    subject: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "message": "File uploaded successfully",
                "file_name": "matematicas_algebra.pdf",
                "file_type": "pdf",
                "subject": "Matemáticas"
            }
        }