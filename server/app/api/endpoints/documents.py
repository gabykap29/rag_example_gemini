from fastapi import APIRouter, Request
from app.services.documents import  upload_pdf 

router = APIRouter()

@router.post("/uploads")
async def upload_file(request: Request):
    form = await request.form()
    file = form["file"]
    subject = form["subject"]
    upload_pdf(file, subject)
    return {"message": "File uploaded successfully"}
