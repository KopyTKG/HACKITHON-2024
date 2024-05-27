import json
import re

def extract_info_from_json(file_path):
    # Načti JSON data ze souboru
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    result = []
    pattern = re.compile(r'/(\d+)/info/')
    
    # Projdi každý záznam v hlavním poli
    for record in data:
        informace = record.get('informace', [])
        
        # Projdi každou položku v poli "informace"
        for info in informace:
            iri = info.get('iri', None)
            if iri:
                match = pattern.search(iri)
                if match:
                    id_info = match.group(1)
                else:
                    id_info = None

            název = info.get('url', {})
            
            if id_info and název:
                result.append([id_info, název])
    
    return result

# Použití funkce s daným souborem
file_path = '/home/alex/Documents/GitHub/HACKITHON-2024/backend/testing/response_1716582009870.json'
info_list = extract_info_from_json(file_path)

# Výpis výsledku
for item in info_list:
    print(item)
