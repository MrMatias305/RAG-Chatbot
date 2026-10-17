from pypdf import PdfReader
from pathlib import Path

from vector_db import store_chunks

PDF_DIR = Path(__file__).parent.parent / "data" / "pdfs"

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


def ingest_documents(chunk_size=300,
					 overlap=50,
					 collection_name="research_documents"):
	"""Ingest all PDFs in chunks"""

	pdf_files = extract_pdfs()

	if not pdf_files:
		print("No PDFs found")

	all_chunks = []
	print(f"Found {len(pdf_files)} PDFs")
	print(f"Chunk size: {chunk_size}")
	print(f"Overlap: {overlap}")
	print(f"Collection name: {collection_name}")

	for pdf in pdf_files:
		pages = extract_text(pdf)

		for page in pages:
			chunks = chunk_text(page["text"], chunk_size, overlap)

			for chunk in chunks:
				all_chunks.append({
					"chunk_id": f"chunk_{len(all_chunks)+1:04d}",
					"source": page["source"],
					"page_number": page["page_number"],
					"text": chunk
				})

	store_chunks(all_chunks, collection_name)
	print(f"Total chunks generated: {len(all_chunks)}")


if __name__ == "__main__":
	ingest_documents(300,
					 50,
					 collection_name="research_documents_300")

