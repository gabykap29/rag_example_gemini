from pydantic import BaseModel
from typing import Optional

class UploadResponse(BaseModel):
    message: str
    
    class Config:
        schema_extra = {
            "example": {
                "message": "File uploaded successfully"
            }
        }