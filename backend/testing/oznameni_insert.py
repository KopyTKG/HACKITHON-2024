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

            nazev = info.get('název', {}).get('cs', None)
            url = info.get('url', None)
            vyveseni = info.get('vyvěšení', {})
            dat_vyveseni = vyveseni.get('datum', None)
            if vyveseni.get('nespecifikovaný', False):
                dat_vyveseni = None
            
            relevantni_do = info.get('relevantní_do', {})
            dat_relevantni_do = relevantni_do.get('datum', None)
            if relevantni_do.get('nespecifikovany', False):
                dat_relevantni_do = None
            
            if id_info and nazev:
                result.append({
                    'id_info': id_info,
                    'nazev': nazev,
                    'url': url,
                    'dat_vyveseni': dat_vyveseni,
                    'dat_relevantni_do': dat_relevantni_do
                })

    return result

def generate_sql_inserts(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for record in data:
            id_info = record['id_info']
            nazev = record['nazev'].replace("'", "''")  # Escaping single quotes for SQL
            url = record['url']
            dat_vyveseni = f"'{record['datum_vyveseni']}'" if record['dat_vyveseni'] else 'NULL'
            dat_relevantni_do = f"'{record['datum_relevantni_do']}'" if record['dat_relevantni_do'] else 'NULL'
            sql = f"INSERT INTO oznameni (id, nazev, url, dat_vyveseni, dat_relevance, id_urad) VALUES (DEFAULT, '{nazev}', '{url}', {dat_vyveseni}, {dat_relevantni_do}, {id_info});\n"
            file.write(sql)

# Příklad použití
data = extract_info_from_json('/home/alex/Documents/GitHub/HACKITHON-2024/backend/testing/response_1716582009870.json')

generate_sql_inserts(data, 'inserts.txt')
