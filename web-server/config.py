import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 16789))
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    LOG_FILE = os.getenv('LOG_FILE', 'data/received_data.json')
    LOG_FORMAT = os.getenv('LOG_FORMAT', 'jsonl')  # 'jsonl' or 'array'
    MAX_LOG_SIZE_MB = int(os.getenv('MAX_LOG_SIZE_MB', 100))