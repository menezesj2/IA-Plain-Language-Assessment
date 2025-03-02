"""
Filename: Automated Textual Analysis.py
Author: Juliana Menezes
Date: 2025-01-06
Description: The script reads PDF documents and calculates readability and similarity metrics for the documents. In the context of this project, I am analysing Initial Project Descriptions (IPDs) and thier Plain Language Summaries (PLSs) created under the Canadian Impact Assessment Act, 2019. The code calculates similarity metrics for each pair of IPD and IDP PLSs.
License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0)
         https://creativecommons.org/licenses/by-nc-sa/4.0/
"""

# Define the path to the PDF folder
pdf_folder = "input_path"

# Check Input Folder
import os

# List all files in the PDF folder
pdf_files = [f for f in os.listdir(pdf_folder) if os.path.isfile(os.path.join(pdf_folder, f))]
print(len(pdf_files))
print(pdf_files)

# Define the path to the results output folder
output_folder = "output_path"
