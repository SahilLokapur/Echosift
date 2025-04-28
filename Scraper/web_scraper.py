import requests
from bs4 import BeautifulSoup
from newspaper import Article
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import spacy

# Initialize spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize NLTK
nltk.download('punkt')


def remove_boilerplate(content):
    """Removes boilerplate content like ads or navigation menus."""
    article = Article(content)
    article.download()
    article.parse()
    return article.text


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
    """Preprocess text by removing boilerplate, tokenization, and chunking."""
    clean_text = remove_boilerplate(text)
    words, sentences = tokenize_text(clean_text)
    chunks = chunk_text(clean_text)

    return {
        "clean_text": clean_text,
        "words": words,
        "sentences": sentences,
        "chunks": chunks
    }


def scrape_website(url, preprocess=False):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, "lxml")
    text = ' '.join([p.get_text() for p in soup.find_all('p')])

    if preprocess:
        preprocessed_data = preprocess_text(text)
        return {"text": text, "preprocessed_data": preprocessed_data, "source": url}
    else:
        return {"text": text, "source": url}
