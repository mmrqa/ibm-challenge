import docx
import pdfplumber

def extract_docx_clauses(file):
    doc = docx.Document(file)
    return [p.text.strip() for p in doc.paragraphs if p.text.strip()]

def extract_pdf_clauses(file):
    text = ''
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return [p.strip() for p in text.split("\n\n") if p.strip()]

import re

def split_clause_into_chunks(text, max_length=2048):
    """
    Splits a long clause into chunks <= max_length characters,
    attempting to split on sentence boundaries.
    """
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) + 1 <= max_length:
            current += sentence + " "
        else:
            chunks.append(current.strip())
            current = sentence + " "

    if current:
        chunks.append(current.strip())

    return chunks