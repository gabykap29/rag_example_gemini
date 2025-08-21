from app.config.config import pdf_directory
from app.core.documents import is_pdf_already_indexed

from app.core.documents import load_pdf, index_docs, retrieve_docs


def upload_pdf(file, subject):
    with open(pdf_directory + file.name, "wb") as f:
        f.write(file.getbuffer())
        file_path = pdf_directory + file.name
        if is_pdf_already_indexed(file_path, subject):
            return "PDF already indexed"
        else:
            documents = load_pdf(file_path)
            index_docs(documents, subject)
            return "PDF indexed successfully"

#Funcion para obtener los documentos
def retrieve(query, subject): 
    documents = retrieve_docs(query, subject)
    return documents

