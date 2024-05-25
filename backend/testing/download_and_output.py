import re
import PyPDF2
import requests
import tempfile
import os

def download_and_extract_pdf_text(url):
    """
    Downloads a PDF from the given URL, extracts text from it, and returns the text.

    :param url: The URL of the PDF to download.
    :return: The extracted text from the PDF.
    """
    # Download the file
    response = requests.get(url)

    if response.status_code == 200:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(response.content)
            temp_file_path = temp_file.name

        print("File downloaded successfully to temporary file.")

        try:
            # Read the temporary file
            with open(temp_file_path, 'rb') as file:
                # Create a PDF file reader object
                pdf_reader = PyPDF2.PdfReader(file)

                # Get the total number of pages in the PDF
                num_pages = len(pdf_reader.pages)

                # Extract text from each page and store it in a list
                extracted_text = []
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    extracted_text.append(text)

            # Combine all the extracted text into a single string
            full_text = "\n".join(extracted_text)

        finally:
            # Delete the temporary file
            os.remove(temp_file_path)
            print("Temporary file deleted.")

        return full_text
    else:
        print("Failed to download file.")
        return None


import re
import requests

def find_line_with_word(text, word):
    # Create a regex pattern to match any occurrence of the word
    pattern = re.compile(re.escape(word), re.IGNORECASE | re.DOTALL)
    
    # Search for the pattern in the text
    match = pattern.search(text)
    
    if match:
        # If a match is found, return the entire line
        start_index = text.rfind('\n', 0, match.start()) + 1
        end_index = text.find('\n', match.end())
        line = text[start_index:end_index]
        return line
    else:
        # If no match is found, return False
        return False

kraje = ['Karlovar', 'Plze', 'Úste', 'Liber', 'Prah', 'Středo', 'Jiho', 'Králov', 'Pardub', 'Vysočin', 'Jiho', 'Olomou', 'Zlín', 'Morav']


url = "https://www.mvcr.cz/soubor/sbirka-jihomoravskeho-kraje-pomoc-obcim-jihomoravskeho-kraje-zasazenym-dne-24-6-2021-extremnimi-bourkami-a-zmirneni-skodlivych-nasledku-na-zdravi-majetku-a-zivotnim-prostredi.aspx"
pdf_text = download_and_extract_pdf_text(url)

for kraj in kraje:
    result = find_line_with_word(pdf_text, kraj)
    if result:
        print(f"Non-false response for '{kraj}': {result}")
