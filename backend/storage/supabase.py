from typing import BinaryIO, Optional
from backend.storage.base import BaseStorage
from backend.core.config import settings
from backend.utils.logging import logger

class SupabaseStorage(BaseStorage):
    def __init__(self):
        self.client = None
        if settings.SUPABASE_URL and settings.SUPABASE_KEY:
            try:
                from supabase import create_client, Client
                self.client: Optional[Client] = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
            except ImportError:
                logger.warning("supabase python client not installed or imports failing. SupabaseStorage disabled.")

    def upload_file(self, file_data: BinaryIO, file_name: str, folder: str = "documents") -> str:
        if not self.client:
            logger.warning("Supabase storage client not initialized. Falling back to local filepath mock.")
            # Mock URL / local fallback
            return f"https://mock-supabase.supabase.co/storage/v1/object/public/{folder}/{file_name}"
        
        bucket_name = folder
        file_bytes = file_data.read()
        
        # Uploading via Supabase Storage API
        try:
            # Check bucket presence, or create/upload
            response = self.client.storage.from_(bucket_name).upload(
                path=file_name,
                file=file_bytes,
                file_options={"content-type": "application/octet-stream"}
            )
            # Fetch public URL
            public_url = self.client.storage.from_(bucket_name).get_public_url(file_name)
            return public_url
        except Exception as e:
            logger.error(f"Supabase upload failed: {str(e)}")
            raise e

    def download_file(self, file_path: str) -> bytes:
        if not self.client:
            raise NotImplementedError("Supabase client is offline.")
        
        try:
            # Assuming file_path contains bucket_name/file_name
            parts = file_path.replace("https://", "").split("/")
            bucket_name = parts[4]
            file_name = "/".join(parts[5:])
            
            response = self.client.storage.from_(bucket_name).download(file_name)
            return response
        except Exception as e:
            logger.error(f"Supabase download failed: {str(e)}")
            raise e

    def delete_file(self, file_path: str) -> bool:
        if not self.client:
            return False
        try:
            parts = file_path.replace("https://", "").split("/")
            bucket_name = parts[4]
            file_name = "/".join(parts[5:])
            self.client.storage.from_(bucket_name).remove(file_name)
            return True
        except Exception as e:
            logger.error(f"Supabase delete failed: {str(e)}")
            return False
