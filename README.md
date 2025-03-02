# IA Plain Language Assessment Project - Menezes, J (2025)

The main script in this project (_Automated Textual Analysis_.py) reads PDF documents and calculates readability and similarity metrics for the documents. In the context of this project, I am analysing Initial Project Descriptions (IPDs) and thier Plain Language Summaries (PLSs) created under the Canadian _Impact Assessment Act_, 2019. The code calculates similarity metrics for each pair of IPD and IDP PLSs.

### First, we define the path to folder with the PDF documents (Input Folder) and the path to folder where we want to store results (Output Folder).
pdf_folder = "input_path"
output_folder = "output_path"

### We then check the Input Folder to ensure that it is reading the PDFs there
import os
pdf_files = [f for f in os.listdir(pdf_folder) if os.path.isfile(os.path.join(pdf_folder, f))]
print(len(pdf_files))
print(pdf_files)

