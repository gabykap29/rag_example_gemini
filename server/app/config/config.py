from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")


pdf_directory = "./documents"
db_directory = "./app/db"
