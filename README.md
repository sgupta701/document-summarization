# 🧠 Single Document Summarizer

A lightweight backend service for generating summaries from **PDF**, **DOCX**, **TXT**, and **image-based documents (OCR)**.  
Built using **Python**, **Flask**, and **NLP-based summarization**.

---

## 🚀 Features

- Extracts text from:
  - PDF (`pdfplumber`, `fitz`)
  - DOCX (`python-docx`)
  - ODT (`odfpy`)
  - Images (`pytesseract`, `Pillow`)
- Generates concise summaries from the extracted text.
- Easy to deploy and integrate.

---

## 📂 Project Structure

```
single-doc-summarizer/
│
├── api/
│   └── server.py                # Flask API backend
│
├── src/
│   └── single_summarizer_module.py   # Core text extraction & summarization logic
│
├── notebooks/
│   └── 01_single_doc_summarizer.ipynb   # Experimentation / development notebook
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/sgupta701/document-summarization.git
cd document-summarization
```

### 2. Create and activate a virtual environment
Using **conda**:
```bash
conda create -n single-summarizer python=3.10
conda activate single-summarizer
```

Or using **venv**:
```bash
python -m venv venv
venv\Scripts\activate   # on Windows
source venv/bin/activate  # on macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the backend server
```bash
cd api
python server.py
```

By default, Flask runs on:
```
http://127.0.0.1:5000
```

---

## 🔗 API Usage

### **Endpoint:**
```
POST http://127.0.0.1:5000/summarize
```

### **Request:**
Send a file (PDF, DOCX, TXT, or image) via form-data:
```bash
curl -X POST -F "file=@sample.pdf" http://127.0.0.1:5000/summarize
```

### **Response:**
```json
{
  "summary": "This document discusses..."
}
```
---


