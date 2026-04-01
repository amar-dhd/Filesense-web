import re
from transformers import pipeline
from PyPDF2 import PdfReader

# Load the AI model once
summarizer_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

def read_txt(file):
    return file.read().decode("utf-8")

def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + " "
    return text

def clean(text):
    return re.sub(r'\s+', ' ', text).strip()

def ai_summarize(text, max_len=150):
    words = text.split()
    chunks = [" ".join(words[i:i+400]) for i in range(0, len(words), 400)]

    summary = ""
    for chunk in chunks:
        res = summarizer_pipeline(
            chunk,
            max_length=max_len,
            min_length=40,
            do_sample=False
        )
        summary += res[0]["summary_text"] + " "

    return summary.strip()
