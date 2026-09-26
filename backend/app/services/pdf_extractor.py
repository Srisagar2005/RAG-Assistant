import fitz
from pathlib import Path


class PDFExtractionError(Exception):
    """Raised when a PDF can't be opened or read (corrupt, encrypted, etc.)."""


def extract_text(pdf_path: Path) -> str:
    try:
        document = fitz.open(pdf_path)
    except Exception as e:
        raise PDFExtractionError(f"Could not open PDF: {e}") from e

    try:
        text = ""
        for page in document:
            text += page.get_text()
    except Exception as e:
        raise PDFExtractionError(f"Could not read PDF content: {e}") from e
    finally:
        document.close()

    return text