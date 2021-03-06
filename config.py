import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.environ.get("API_ID", "0"))
    API_HASH = os.environ.get("API_HASH", "")
    CHAT_ID = int(os.environ.get("CHAT_ID", "0"))
    SESSION_STRING = os.environ.get("SESSION_STRING", "")

class Database:
    VIDEO_CALL = {}
    RADIO_CALL = {}
    FFMPEG_PROCESSES = {}