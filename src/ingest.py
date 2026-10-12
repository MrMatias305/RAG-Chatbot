from pypdf import PdfReader
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = PROJECT_DIR / "data" / "pdfs"

file_path = f"{PDF_DIR}/cv.pdf"
reader = PdfReader(str(file_path))

for page_num, page in enumerate(reader.pages, start=1):
	text = page.extract_text() or ""
	print(text)

