import PyPDF2
import os
import requests

# Hardcoded URL and file path
url = "https://www.hzscr.cz/soubor/vyrocni-zprava-2019-podle-106-pdf.aspx"
file_path = "C:/Users/adaml/Desktop/hackithon_2024/data/vyrocni_zprava_2019.pdf"

# Download the file
response = requests.get(url)

if response.status_code == 200:
    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    # Write the content to the file
    with open(file_path, 'wb') as f:
        f.write(response.content)
    print("File downloaded successfully.")
else:
    print("Failed to download file.")

# Read the downloaded file
with open(file_path, 'rb') as file:
    # Create a PDF file reader object
    pdf_reader = PyPDF2.PdfReader(file)

    # Get the total number of pages in the PDF
    num_pages = len(pdf_reader.pages)

    # Iterate through each page and extract text
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()

        # Print the text from the current page
        print("Page", page_num + 1, ":", text)