import pdfplumber
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import nltk
import spacy
from nltk.tokenize import word_tokenize, sent_tokenize

# Initialize spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize NLTK
nltk.download('punkt')


def tokenize_text(text):
    """Tokenize the text into words and sentences."""
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    return words, sentences


def chunk_text(text):
    """Perform named entity recognition or noun phrase chunking."""
    doc = nlp(text)
    chunks = []
    for chunk in doc.noun_chunks:
        chunks.append(chunk.text)
    return chunks


def preprocess_text(text):
    """Preprocess text by tokenization and chunking."""
    words, sentences = tokenize_text(text)
    chunks = chunk_text(text)

    return {
        "words": words,
        "sentences": sentences,
        "chunks": chunks
    }


def scrape_pdf(uploaded_file, preprocess=False):
    text = ""
    try:
        # Attempt to extract text using pdfplumber (for regular PDFs)
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception as e:
        text = ""

    # If no text was extracted, use OCR (for scanned PDFs)
    if not text.strip():
        images = convert_from_path(uploaded_file)
        for image in images:
            text += pytesseract.image_to_string(image)

    if preprocess:
        preprocessed_data = preprocess_text(text)
        return {"text": text, "preprocessed_data": preprocessed_data, "source": uploaded_file.name}
    else:
        return {"text": text, "source": uploaded_file.name}
