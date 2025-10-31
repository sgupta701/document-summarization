import pytesseract
from PIL import Image
import pdfplumber
import fitz  
import docx
from odf import text, teletype, opendocument
import os
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

model_name = "facebook/bart-large-cnn"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)


def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text_data = ""

    if ext == ".pdf":
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_data += page_text + "\n"
            if not text_data.strip():
                pdf_doc = fitz.open(file_path)
                for page_number, page in enumerate(pdf_doc, start=1):
                    pix = page.get_pixmap(dpi=300)
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    ocr_text = pytesseract.image_to_string(img, lang="eng")
                    text_data += f"\n\n--- Page {page_number} ---\n{ocr_text}"
        except Exception as e:
            print("PDF read error:", e)
    elif ext in [".png", ".jpg", ".jpeg"]:
        img = Image.open(file_path)
        text_data = pytesseract.image_to_string(img, lang="eng")
    elif ext == ".docx":
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text_data += para.text + "\n"
    elif ext == ".odt":
        doc = opendocument.load(file_path)
        allparas = doc.getElementsByType(text.P)
        for p in allparas:
            text_data += teletype.extractText(p) + "\n"
    else:
        raise ValueError("Unsupported file type.")

    return text_data.strip()


def generate_summary(text):
    if len(text.split()) < 100:
        result = summarizer(text, max_length=150, min_length=30, do_sample=False)
        return result[0]['summary_text']

    inputs = tokenizer(text, return_tensors="pt", truncation=False)["input_ids"][0]
    max_tokens = 900
    token_chunks = [inputs[i:i + max_tokens] for i in range(0, len(inputs), max_tokens)]

    summaries = []
    for chunk in token_chunks:
        chunk_text = tokenizer.decode(chunk, skip_special_tokens=True)
        summary = summarizer(chunk_text, max_length=250, min_length=80, do_sample=False)
        summaries.append(summary[0]['summary_text'])

    combined_summary = " ".join(summaries)
    if len(summaries) > 1:
        final_summary = summarizer(combined_summary, max_length=300, min_length=100, do_sample=False)
        return final_summary[0]['summary_text']
    else:
        return combined_summary
