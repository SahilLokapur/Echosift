from transformers import pipeline, BartTokenizer
from summa import summarizer  # Added for extractive summarization

# Load the summarizer pipeline and tokenizer
abstractive_summarizer = pipeline("summarization", model="facebook/bart-large-cnn", framework="pt")
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

def preprocess_text(text):
    unwanted_sections = [
        "sales@w3schools.com",
        "help@w3schools.com",
        "Contact us about W3Schools Academy",
        "Join our newsletter",
        "Training After completing this course",
        "solutions architects",
        "Technical professionals"
    ]
    for section in unwanted_sections:
        text = text.replace(section, "")
    return text


def summarize_text_with_summa_and_bart(text, preprocess=False):
    # Step 1: Preprocess the text if needed
    if preprocess:
        preprocessed_text = preprocess_text(text)
    else:
        preprocessed_text = text

    # Step 2: Extractive summary with summa
    extractive_summary = summarizer.summarize(preprocessed_text)

    if not extractive_summary or len(extractive_summary.strip()) == 0:
        return "Summary could not be generated. The text might be too short or uninformative."

    # Step 3: Tokenize and truncate extractive summary based on tokens
    input_ids = tokenizer.encode(extractive_summary, truncation=True, max_length=1024, return_tensors="pt")

    # Step 4: Decode back to truncated text
    truncated_summary = tokenizer.decode(input_ids[0], skip_special_tokens=True)

    # Step 5: Abstractive summary using BART
    abstractive_summary = abstractive_summarizer(truncated_summary, max_length=350, min_length=150, do_sample=False)

    return abstractive_summary[0]['summary_text']
