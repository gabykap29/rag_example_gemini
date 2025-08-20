from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")


pdf_directory = "./server/app/data"
db_directory = "./server/app/db"
