import pdfplumber

pdf_path = r"D:\Homelab\site\gdocs with image\homelab.pdf"

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        print(page.extract_text())