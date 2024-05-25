import json
import re
import PyPDF2
import requests
import tempfile
import os


def download_and_extract_pdf_text(url):
    """
    Downloads a PDF from the given URL, extracts text from it, and returns the text.

    :param url: The URL of the PDF to download.
    :return: The extracted text from the PDF, or None if an error occurs.
    """
    try:
        # Download the file
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for non-200 status codes

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

            return full_text

        finally:
            # Delete the temporary file
            os.remove(temp_file_path)
            print("Temporary file deleted.")

    except Exception as e:
        print(f"Failed to download and extract text from PDF: {e}")
        return None



def find_line_with_word(text, word):
    if text is None:
        return False
    
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




def extract_info_from_json(file_path):
    # Load JSON data from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    result = []
    pattern = re.compile(r'/(\d+)/info/')
    
    # Iterate through each record in the main data structure
    for record in data:
        informace = record.get('informace', [])
        
        # Iterate through each item in the "informace" array
        for info in informace:
            # Check if info is a dictionary
            if isinstance(info, dict):
                # Extract id_info from the 'iri' field using regex pattern
                iri = info.get('iri', None)
                if iri:
                    match = pattern.search(iri)
                    id_info = match.group(1) if match else None

                # Check if 'dokument' field exists and if it's a list
                if 'dokument' in info and isinstance(info['dokument'], list):
                    # Iterate through each item in the 'dokument' list
                    for dokument_item in info['dokument']:
                        # Get the 'url' field from each dokument item
                        doc_url = dokument_item.get('url', None)
                        # Check if all required fields are not None before appending to the result list
                        if id_info and doc_url:
                            result.append([id_info, doc_url])
                else:
                    # Get the 'url' from the 'dokument' dictionary
                    doc_url = info.get('dokument', {}).get('url', None)
                    # Check if all required fields are not None before appending to the result list
                    if id_info and doc_url:
                        result.append([id_info, doc_url])
    
    return result

file_path = '/home/aerceas/Downloads/ministerstvo_vnitra.json'
kraje = ['Karlovar', 'Plze', 'Úste', 'Liber', 'Prah', 'Středo', 'Jiho', 'Králov', 'Pardub', 'Vysočin', 'Jiho', 'Olomou', 'Zlín', 'Morav']
info_list = extract_info_from_json(file_path)

for url in info_list:
    text = download_and_extract_pdf_text(url[1])
    for kraj in kraje:
        result = find_line_with_word(text, kraj)
        if result:
            print(f"Non-false response for '{kraj}': {result}")
# Example usage: printing the doc_url for each info item in the info_list

# pdf_text = download_and_extract_pdf_text(url)
# print(pdf_text)


# ukazka toho, jak funguje download and extract -> if text exists -> returns text if not -> atom bomb
#pdf_text = download_and_extract_pdf_text(url)

#find_line_with_word -> dostane pdf file + kraje. Vrací False, pokud nenajde jinak vrací jaké všechny kraje to našlo
# Použití funkce s daným souborem
#Info list -> všechny id a url. url index [1]
