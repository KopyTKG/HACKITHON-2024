import PyPDF2
import os
import requests

def download_and_extract_text(url, file_path):
    """
    Downloads a PDF from the given URL and extracts text from each page.
    
    Args:
    url (str): The URL of the PDF to download.
    file_path (str): The local file path where the PDF will be saved.
    
    Returns:
    str: The extracted text from the PDF.
    """
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

    extracted_text = ""
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

            # Append the text from the current page
            extracted_text += text

    return extracted_text

# Example usage
url = "https://www.hzscr.cz/soubor/vyrocni-zprava-2019-podle-106-pdf.aspx"
file_path = "home/aerceas/Documents/vyrocni_zprava_2019.pdf"
pdf_text = download_and_extract_text(url, file_path)
print(pdf_text)  # Print the extracted text
