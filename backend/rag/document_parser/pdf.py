import os
from typing import BinaryIO
from backend.utils.logging import logger

class PDFParser:
    @staticmethod
    def extract_text(file_data: BinaryIO, file_name: str) -> str:
        """
        Parses text content from PDF file using pypdf.
        Falls back to standard text decoding if it is a .txt file.
        """
        _, ext = os.path.splitext(file_name.lower())
        
        if ext == ".txt":
            try:
                content = file_data.read()
                # Return decoded string
                if isinstance(content, bytes):
                    return content.decode("utf-8", errors="ignore")
                return str(content)
            except Exception as e:
                logger.error(f"Failed to parse text file: {str(e)}")
                return ""
                
        elif ext == ".pdf":
            try:
                from pypdf import PdfReader
                reader = PdfReader(file_data)
                text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                return text.strip()
            except ImportError:
                logger.error("pypdf is not installed. PDF parsing failed.")
                return "[Error: pypdf not available for processing]"
            except Exception as e:
                logger.error(f"PDF extraction failed: {str(e)}")
                return ""
        else:
            # Fallback string read
            try:
                return file_data.read().decode("utf-8", errors="ignore")
            except Exception:
                return f"[Unsupported binary content: {file_name}]"
