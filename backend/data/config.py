
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
os.makedirs(INSTANCE_DIR, exist_ok=True)

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "secret-key")

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" + os.path.join(INSTANCE_DIR, "cuad.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DATA_FOLDER = os.path.join(BASE_DIR, "data")