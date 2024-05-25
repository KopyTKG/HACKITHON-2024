import json
import re
import PyPDF2
import requests
import tempfile
import os
import traceback

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
    i = 0

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
                nazev = info.get('název', {}).get('cs', None)
                vyveseni = info.get('vyvěšení', {}).get('datum', None)
                relevance_1 = info.get('relevantní_do', {}).get('datum', None)
                id = i
                if relevance_1:
                    relevance_1 = False
                # Check if 'dokument' field exists and if it's a list
                if 'dokument' in info and isinstance(info['dokument'], list):
                    # Iterate through each item in the 'dokument' list
                    for dokument_item in info['dokument']:
                        # Get the 'url' field from each dokument item
                        nazev = dokument_item.get('název', {}).get('cs', None)
                        doc_url = dokument_item.get('url', None)

                        # Check if all required fields are not None before appending to the result list
                        if id_info and doc_url:
                            result.append([id_info, doc_url, nazev, vyveseni, relevance_1, id, nazev, doc_url])
                else:
                    # Get the 'url' from the 'dokument' dictionary
                    doc_url = info.get('dokument', {}).get('url', None)
                    # Check if all required fields are not None before appending to the result list
                    if id_info and doc_url:
                        result.append([id_info, doc_url, nazev, vyveseni, relevance_1])

                i += 1

    return result


def write_result_to_file(file_path, info_list, kraje, kraj_urls):
    with open(file_path, "w") as file:
        lines_to_write = []
        print(info_list)
        for url_info in info_list:
            print(url_info[0])
            kraj = function(url_info[0])

            # id, nazev, url, uredni_deska, datum_vyveseni, datum_relevance
            file.write(f"INSERT INTO oznameni (id, nazev, url, urad_id, datum_vyveseni, datum_relevance) VALUES ({url_info[5]}, {url_info[2]},  {url_info[1]}, {kraj}, {url_info[3]}, {url_info[4]}),\n")

            #file.write(f"INSERT INTO dokument (id, nazev, url, oznameni_id) VALUES (DEFAULT, {url_info[6]},  {url_info[7]}, {url_info[5]}\n")


        #     url = url_info[1]
        #     for kraj_index, kraj in enumerate(kraje):
        #
        #         if kraj in url_info[0]:
        #             kraj_urls[f'kraj_{kraj_index}'].append(url)
        #             lines_to_write.append(f"ID: {url_info[0]}, URL: {url}, Kraj: {kraj}\n")
        #             break  # Once matched, no need to continue checking other regions
        # file.writelines(lines_to_write)



# Define the list of 'kraje'
kraje = ['Karlovar', 'Plze', 'Úste', 'Liber', 'Prah', 'Středo', 'Jiho', 'Králov', 'Pardub', 'Vysočin', 'Jiho', 'Olomou',
         'Zlín', 'Morav']

data = """
0 - 10017
1 - 10018
2 - 10015
3 - 10016
4 - 10014
5 - 10019
6 - 10023
7 - 10020
8 - 10021
9 - 10022
10 - 10024
11 - 10025
12 - 10026
13 - 10027
"""

# Creating the list of tuples
data_list = []
for line in data.strip().split("\n"):
    name, code = line.split(" - ")
    data_list.append((name, code))

def function(city):
    for name, code in data_list:
        if name == city:
            return code
    print('finish')  # Return None if city is not found


# Initialize a dictionary to store lists of URLs for each 'kraj'
kraj_urls = {f'kraj_{i}': [] for i in range(len(kraje))}

file_path = '/home/sabinaaj/Downloads/pcr.json'
info_list = extract_info_from_json(file_path)

for url_info in info_list:
    try:
        text = download_and_extract_pdf_text(url_info[1])
        for kraj_index, kraj in enumerate(kraje):
            if text and kraj in text:
                kraj_urls[f'kraj_{kraj_index}'].append(url_info[1])
    except Exception as e:
        print(f"Failed to process URL: {url_info[1]}")
        traceback.print_exc()

# Writing the result to a file
write_result_to_file("/home/sabinaaj/Downloads/pcr.txt", info_list, kraje, kraj_urls)
# pdf_text = download_and_extract_pdf_text(url)
# print(pdf_text)


# ukazka toho, jak funguje download and extract -> if text exists -> returns text if not -> atom bomb
#pdf_text = download_and_extract_pdf_text(url)

#find_line_with_word -> dostane pdf file + kraje. Vrací False, pokud nenajde jinak vrací jaké všechny kraje to našlo
# Použití funkce s daným souborem
#Info list -> všechny id a url. url index [1]
