import os
import shutil
from typing import BinaryIO
from backend.storage.base import BaseStorage
from backend.core.config import settings

class LocalStorage(BaseStorage):
    def __init__(self):
        self.base_dir = settings.LOCAL_STORAGE_DIR
        os.makedirs(self.base_dir, exist_ok=True)

    def upload_file(self, file_data: BinaryIO, file_name: str, folder: str = "documents") -> str:
        folder_path = os.path.join(self.base_dir, folder)
        os.makedirs(folder_path, exist_ok=True)
        
        file_path = os.path.join(folder_path, file_name)
        # Handle duplicate filenames
        base, extension = os.path.splitext(file_name)
        counter = 1
        while os.path.exists(file_path):
            file_path = os.path.join(folder_path, f"{base}_{counter}{extension}")
            counter += 1

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file_data, buffer)
            
        # Return path relative to base directory or absolute path
        return os.path.abspath(file_path)

    def download_file(self, file_path: str) -> bytes:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, "rb") as buffer:
            return buffer.read()

    def delete_file(self, file_path: str) -> bool:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                return True
            except OSError:
                return False
        return False
