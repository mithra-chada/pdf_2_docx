import os
from pdf2docx import Converter
from typing import Optional

class PDFConverter:
    def __init__(self):
        pass

    def convert(self, pdf_path: str, docx_path: str, start: int = 0, end: Optional[int] = None):
        """
        Converts a PDF file to a DOCX file while preserving layout.
        
        Args:
            pdf_path (str): Path to the source PDF file.
            docx_path (str): Path to the destination DOCX file.
            start (int): Start page (0-based).
            end (int): End page (None for all).
        """
        try:
            cv = Converter(pdf_path)
            cv.convert(docx_path, start=start, end=end)
            cv.close()
            return True, "Conversion successful"
        except Exception as e:
            return False, str(e)

if __name__ == "__main__":
    # Test
    pass
