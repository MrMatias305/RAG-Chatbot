from pypdf import PdfReader
from pathlib import Path

from vector_db import store_chunks

PDF_DIR = Path(__file__).parent.parent / 'data/pdfs'

def extract_pdfs():
	"""Get all PDFs found in PDF_DIR"""

	pdf_files = list(PDF_DIR.glob('*.pdf'))
	return pdf_files


def clean_text(text):
	"""Clean text from PDFs"""
	return " ".join(text.split())


def extract_text(pdf_path):
	"""Extract text from PDFs"""

	reader = PdfReader(str(pdf_path))
	pages = []

	for page_num, page in enumerate(reader.pages, start=1):
		text = page.extract_text() or ""
		text = clean_text(text)
		pages.append({
			"source": pdf_path.name,
			"page_number": page_num,
			"text": text
		})
	return pages


def chunk_text(text, chunk_size=300, overlap=50):
	"""Split text into chunks of size chunk_size"""

	chunks = []
	words = text.split()
	start = 0

	while start < len(words):
		end = start + chunk_size
		chunk = " ".join(words[start:end])
		chunks.append(chunk)
		start += chunk_size - overlap

	return chunks


if __name__ == "__main__":

	if not extract_pdfs():
		print("No PDFs found")
	else:
		all_chunks = []
		print("Found {} PDFs".format(len(extract_pdfs())))

		for pdf in extract_pdfs():
			pages = extract_text(pdf)

			for page in pages:
				chunks = chunk_text(page["text"])

				for chunk in chunks:
					chunk_id = f"chunk_{len(all_chunks)+1:04d}"
					all_chunks.append({
						"chunk_id": chunk_id,
						"source": page["source"],
						"page_number": page["page_number"],
						"text": chunk
					})

		store_chunks(all_chunks)


