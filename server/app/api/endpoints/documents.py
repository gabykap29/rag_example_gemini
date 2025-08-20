from fastapi import APIRouter, Request
from services.documents import retrieve_docs, upload_pdf, load_pdf 

router = APIRouter()

@router.post("/uploads")
async def upload_file(request: Request):
    form = await request.form()
    file = form["file"]
    subject = form["subject"]
    upload_pdf(file, subject)
    return {"message": "File uploaded successfully"}

