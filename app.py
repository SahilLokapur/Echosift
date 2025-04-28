import sys
import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from io import BytesIO

from Scraper.web_scraper import scrape_website
from Scraper.pdf_scraper import scrape_pdf
# from utils.export import export_data # Removed the direct import
from nlp.summarizer import summarize_text_with_summa_and_bart
from nlp.qna_bot import ask_question
from nlp.keyword_extractor import extract_keywords
from utils.security import check_redirects, detect_rate_limit

# ----------------- Streamlit Page Config -----------------
st.set_page_config(page_title="EchoSift", layout="wide")

# ----------------- Custom CSS -----------------
st.markdown("""
<style>
    .stApp {
        background-color: #1E1E1E;
    }
    h1, h2, h3, h4, h5, h6, p, label, div, span, a {
        color: #FAFAFA !important;
    }
    .card {
        background-color: #2D2D2D;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.5);
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #FF5E5B;
        color: white;
        border-radius: 10px;
    }
    .stButton>button:hover {
        background-color: #FF7B7B;
        color: white;
    }
    .stTextInput>div>div>input, .stTextArea textarea {
        background-color: #3A3A3A;
        color: #FAFAFA;
    }
    /* Target all text elements within the sidebar */
    .st-emotion-cache-16txtl3 { /* This class might be dynamically generated, but often appears */
        color: black !important;
    }
    .st-emotion-cache-h5rgaw { /* Another common class for sidebar text */
        color: black !important;
    }
    .st-emotion-cache-6qob1r { /* Class for the radio button labels */
        color: black !important;
    }
    .st-emotion-cache-ii0444 { /* Class for the sidebar title */
        color: black !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- Sidebar -----------------
with st.sidebar:
    st.title("📦 EchoSift Menu")
    menu = st.radio("Select Mode", ["Web Scraping", "PDF Extraction"])

# ----------------- Main -----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.title("📦 EchoSift: Data Extraction & Secure Transfer")

# ----------------- Common Functions -----------------
def extract_images(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        images = [urljoin(url, img.get("src")) for img in soup.find_all("img") if img.get("src")]
        return images
    except Exception as e:
        st.error(f"Error extracting images: {e}")
        return []

def export_data_as_csv(data, filename="extracted_data.csv"):
    """Exports a dictionary of data to a CSV file for download."""
    df = pd.DataFrame([data])
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False, encoding='utf-8')
    csv_buffer.seek(0)
    st.download_button(
        label="Download as CSV",
        data=csv_buffer,
        file_name=filename,
        mime="text/csv",
    )

# ----------------- Main Logic -----------------
if menu == "Web Scraping":
    url = st.text_input("Enter website URL")

    if url and st.button("🔍 Extract Website Data"):
        try:
            response = requests.get(url)
            safe, message = check_redirects(response)
            if not safe:
                st.error(f"Security Warning: {message}")
            else:
                data = scrape_website(url)
                st.session_state["web_data"] = data
                st.success("Website data extracted successfully!")
        except Exception as e:
            st.error(f"Failed to extract: {str(e)}")

    if "web_data" in st.session_state:
        data = st.session_state["web_data"]

        tab1, tab2, tab3, tab4 = st.tabs(["Raw Text", "Summary", "Keywords", "Images"])

        with tab1:
            st.subheader("🔢 Raw Extracted Content")
            st.text_area("Website Raw Text", data["text"], height=300)
            export_data_as_csv({"raw_text": data["text"], "source": data.get("source", url)}, filename="raw_text.csv")

        with tab2:
            st.subheader("🌐 Summarization")
            if st.button("Summarize Website Content"):
                summary = summarize_text_with_summa_and_bart(data["text"], preprocess=True)
                st.success("Summary Generated")
                st.text_area("Summary", summary, height=250)
                export_data_as_csv({"summary": summary, "source": data.get("source", url)}, filename="summary.csv")

        with tab3:
            st.subheader("🔑 Keyword Extraction")
            if st.button("Extract Keywords"):
                keywords = extract_keywords(data["text"])
                st.success("Keywords Extracted")
                st.write(keywords)
                export_data_as_csv({"keywords": ", ".join(keywords), "source": data.get("source", url)}, filename="keywords.csv")

        with tab4:
            st.subheader("🖼️ Images")
            if st.button("Extract Images"):
                images = extract_images(url)
                if images:
                    st.success(f"Found {len(images)} images!")
                    for img_link in images[:10]:
                        st.image(img_link, width=150)
                    export_data_as_csv({"image_links": images, "source": url}, filename="image_links.csv")
                else:
                    st.warning("No images found or failed to extract.")

elif menu == "PDF Extraction":
    file = st.file_uploader("Upload a PDF File", type=["pdf"])

    if file and st.button("📂 Extract PDF Data"):
        try:
            data = scrape_pdf(file)
            st.session_state["pdf_data"] = data
            st.success("PDF data extracted successfully!")
        except Exception as e:
            st.error(f"Failed to extract: {str(e)}")

    if "pdf_data" in st.session_state:
        data = st.session_state["pdf_data"]

        tab1, tab2, tab3 = st.tabs(["Raw Text", "Summary", "Keywords"])

        with tab1:
            st.subheader("🔢 Raw PDF Content")
            st.text_area("PDF Raw Text", data["text"], height=300)
            export_data_as_csv({"raw_text": data["text"], "source": data.get("source", file.name)}, filename="pdf_raw_text.csv")

        with tab2:
            st.subheader("🌐 Summarization")
            if st.button("Summarize PDF Content"):
                summary = summarize_text_with_summa_and_bart(data["text"], preprocess=True)
                st.success("Summary Generated")
                st.text_area("Summary", summary, height=250)
                export_data_as_csv({"summary": summary, "source": data.get("source", file.name)}, filename="pdf_summary.csv")

        with tab3:
            st.subheader("🔑 Keyword Extraction")
            if st.button("Extract PDF Keywords"):
                keywords = extract_keywords(data["text"])
                st.success("Keywords Extracted")
                st.write(keywords)
                export_data_as_csv({"keywords": ", ".join(keywords), "source": data.get("source", file.name)}, filename="pdf_keywords.csv")

# ----------------- Q&A Section (Common) -----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🧠 Ask Questions from Extracted Content")
context = st.text_area("Paste context (any extracted text)")
question = st.text_input("Type your Question")
if st.button("🔍 Ask"):
    if context.strip() == "" or question.strip() == "":
        st.warning("Both Context and Question are required!")
    else:
        try:
            answer = ask_question(context, question)
            st.success(f"Answer: {answer}")
        except Exception as e:
            st.error(f"Failed to find answer: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)