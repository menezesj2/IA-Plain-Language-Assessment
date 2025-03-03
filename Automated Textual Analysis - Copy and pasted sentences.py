"""
Filename: Automated Textual Analysis - Copy and pasted sentences.py
Author: Juliana Menezes
Date: 2025-01-06
Description: The script reads PDF documents and calculates readability and similarity metrics for the documents. In the context of this project, I am analysing Initial Project Descriptions (IPDs) and thier Plain Language Summaries (PLSs) created under the Canadian Impact Assessment Act, 2019. The code calculates similarity metrics for each pair of IPD and IDP PLSs.
License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0)
         https://creativecommons.org/licenses/by-nc-sa/4.0/
"""

!pip install nltk pdfplumber

import os
import re
import csv
import nltk
import pdfplumber
from nltk.tokenize import sent_tokenize, word_tokenize

# Download required NLTK data (only needed once)
nltk.download('punkt')
nltk.download('punkt_tab')

import pdfplumber
import pandas as pd
import re
import os

# Define input and output directories
input_dir = "Path to folder with PDF documents"
output_dir = "Path to Sentence Excels Folder"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to process a single PDF file
def process_pdf(pdf_path, output_dir):
    try:
        # Extract text from PDF
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text + "\n"

        # Split text into sentences while maintaining proper sentence boundaries
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text.strip())

        # Remove unwanted line breaks within sentences
        sentences = [re.sub(r'\n', ' ', sentence).strip() for sentence in sentences]

        # Create DataFrame
        df_sentences = pd.DataFrame(sentences, columns=["Sentence"])

        # Get output file path
        pdf_filename = os.path.basename(pdf_path).replace(".pdf", ".xlsx")
        excel_path = os.path.join(output_dir, pdf_filename)

        # Save to Excel
        df_sentences.to_excel(excel_path, index=False)

        print(f"Processed: {pdf_filename}")

    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")

# Loop through all PDF files in the input directory
for filename in os.listdir(input_dir):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(input_dir, filename)
        process_pdf(pdf_path, output_dir)

print("Processing complete. All Excel files are saved.")


import pandas as pd
import os
import re
from difflib import SequenceMatcher

# Define directories
sentence_excels_dir = output_dir
output_file = "Path for results folder/Summary_Match_Results.xlsx"

# Get all Excel files
files = [f for f in os.listdir(sentence_excels_dir) if f.endswith(".xlsx")]

# Identify project pairs
project_pairs = {}
for filename in files:
    if filename.endswith("_Initial Project Description Summary.xlsx"):
        project_name = filename.replace("_Initial Project Description Summary.xlsx", "")
        full_doc_filename = project_name + "_Initial Project Description.xlsx"
        if full_doc_filename in files:
            project_pairs[project_name] = {
                "summary_file": os.path.join(sentence_excels_dir, filename),
                "full_file": os.path.join(sentence_excels_dir, full_doc_filename)
            }

# Function to get the longest common subsequence (LCS) of words
def longest_common_subsequence(a, b):
    """Find the longest common sequence of words between two sentences."""
    words_a = a.split()
    words_b = b.split()

    # Create a sequence matcher
    matcher = SequenceMatcher(None, words_a, words_b)
    match_blocks = matcher.get_matching_blocks()

    # Extract longest matching word sequence
    longest_match = max((words_a[m.a:m.a + m.size] for m in match_blocks if m.size >= 6), key=len, default=[])

    return " ".join(longest_match)

# Function to check if a sentence is copied (6+ word sequence match)
def is_sentence_copied(summary_sentence, full_sentences):
    for full_sentence in full_sentences:
        lcs = longest_common_subsequence(summary_sentence.lower(), full_sentence.lower())
        if len(lcs.split()) >= 6:  # Require 6+ words in sequence to count as copied
            return True
    return False

# Analyze matches
match_results = []
for project, paths in project_pairs.items():
    # Read Excel files
    df_summary = pd.read_excel(paths["summary_file"])
    df_full = pd.read_excel(paths["full_file"])

    # Extract sentences
    summary_sentences = df_summary["Sentence"].astype(str).tolist()
    full_sentences = df_full["Sentence"].astype(str).tolist()  # Keep full sentences separate for matching

    # Count sentences
    num_summary_sentences = len(summary_sentences)
    num_copied_sentences = sum(1 for sent in summary_sentences if is_sentence_copied(sent, full_sentences))

    # Save results
    match_results.append({
        "Project": project,
        "Total Summary Sentences": num_summary_sentences,
        "Copied Sentences": num_copied_sentences,
        "Copied Percentage": round((num_copied_sentences / num_summary_sentences) * 100, 2) if num_summary_sentences > 0 else 0
    })

# Save results to an Excel file
df_results = pd.DataFrame(match_results)
df_results.to_excel(output_file, index=False)

print(f"Analysis complete. Results saved at: {output_file}")
