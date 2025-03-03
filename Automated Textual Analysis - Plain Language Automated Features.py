"""
Filename: Automated Textual Analysis - Plain Language Automated Features.py
Author: Juliana Menezes
Date: 2025-01-06
Description: The script reads PDF documents and calculates readability and similarity metrics for the documents. In the context of this project, I am analysing Initial Project Descriptions (IPDs) and thier Plain Language Summaries (PLSs) created under the Canadian Impact Assessment Act, 2019. The code calculates similarity metrics for each pair of IPD and IDP PLSs.
License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0)
         https://creativecommons.org/licenses/by-nc-sa/4.0/
"""

# Installing necessary modules
!pip install pdfplumber nltk sentence-transformers


import os
import re
import pdfplumber
import pandas as pd
import torch
import nltk
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# Use GPU if available
if torch.cuda.is_available():
    device_index = torch.cuda.current_device()  # Get device index
    device = f"cuda:{device_index}"  # Construct device string
else:
    device = "cpu"

print(f"🔥 Running on {device.upper()}")

# Ensure NLTK resources are available
nltk.download("punkt")
nltk.download("punkt_tab")

# Load optimized BERT model on GPU
model = SentenceTransformer("all-MiniLM-L6-v2").to(device)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define paths
input_folder = "Path to Input Folder"
output_file = "Path Output Folder"

# Function to extract and clean text from PDFs
def extract_clean_text(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = " ".join(page.extract_text() or "" for page in pdf.pages)

        # Clean the text
        text = re.sub(r"(?i)Page \d+|©.*?|Table of Contents", "", text)
        text = re.sub(r"(?i)Figure \d+:.*|Table \d+:.*", "", text)
        text = re.sub(r"(?i)References\s*.*$", "", text, flags=re.MULTILINE)
        text = re.sub(r"\s+", " ", text).strip()
        return text
    except Exception as e:
        print(f"❌ Error extracting text from {pdf_path}: {e}")
        return None

# Function to classify sentences
def classify_sentences(sentences, labels):
    results = classifier(sentences, labels, multi_label=True)
    scores = {label: sum(res["scores"][res["labels"].index(label)] for res in results) / len(sentences) for label in labels}
    return scores

# Analyze PDFs in the folder
data = []
labels = ["Nominalization", "Noun String", "Passive Voice"]

pdf_files = [f for f in os.listdir(input_folder) if "Initial Project Description Summary" in f and f.endswith(".pdf")]

for pdf_file in pdf_files:
    print(pdf_file)
    text = extract_clean_text(os.path.join(input_folder, pdf_file))
    if text:
        sentences = nltk.tokenize.sent_tokenize(text)
        scores = classify_sentences(sentences, labels)

        data.append({
            "Filename": pdf_file,
            "Total Sentences": len(sentences),
            "Nominalization %": scores["Nominalization"] * 100,
            "Noun String %": scores["Noun String"] * 100,
            "Passive Voice %": scores["Passive Voice"] * 100
        })

# Save results to an Excel file
df = pd.DataFrame(data)
df.to_excel(output_file, index=False)
print(f"✅ Analysis complete. Results saved to {output_file}")
