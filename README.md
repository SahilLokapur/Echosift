# Echosift
EchoSift: Data Extraction and Secure Transfer
EchoSift is a powerful, dark-themed web application built with Streamlit that provides end-to-end solutions for:

Web scraping: Extract clean, readable text and images from any public website.

PDF extraction: Extract text from both digital and scanned PDF files.

Summarization: Generate meaningful summaries using a hybrid extractive-abstractive AI approach (Summa + BART model).

Keyword Extraction: Extract important named entities and keywords from the content.

Question-Answering (Q&A): Ask questions from the extracted content and get intelligent answers using a RoBERTa-based QA model.

Security Checks: Detect honeypot websites or rate-limited sites before scraping.

Data Export: Download extracted data as CSV or JSON files easily.

Frontend: Streamlit

Backend: Python (requests, BeautifulSoup, pdfplumber, PyTesseract, spaCy, transformers)

NLP Models:

RoBERTa (for Question-Answering)

BART (for Abstractive Summarization)

Summa (for Extractive Summarization)
