from abc import ABC, abstractmethod
from typing import BinaryIO

class BaseStorage(ABC):
    @abstractmethod
    def upload_file(self, file_data: BinaryIO, file_name: str, folder: str = "documents") -> str:
        """
        Uploads a file to the storage provider.
        Returns the public URL or relative file path.
        """
        pass

    @abstractmethod
    def download_file(self, file_path: str) -> bytes:
        """
        Downloads a file from the storage provider.
        Returns bytes content of the file.
        """
        pass

    @abstractmethod
    def delete_file(self, file_path: str) -> bool:
        """
        Deletes a file from the storage provider.
        Returns True if successful, False otherwise.
        """
        pass
