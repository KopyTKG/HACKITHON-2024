import requests
from unidecode import unidecode

def get_board_names():
    base_url = "https://opendata-test.mvcr.cz/api/boards/"
    names = []
    for board_id in range(1, 183):  # Iterate from 1 to 182 inclusive
        url = f"{base_url}{board_id}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if "informace" in data and len(data["informace"]) > 0:
                for info in data["informace"]:
                    if "název" in info and "cs" in info["název"]:
                        names.append([board_id, info["název"]["cs"]])
                    else:
                        print(f"Board ID {board_id}: No 'název' found")
            else:
                print(f"Board ID {board_id}: No 'informace' found")
        else:
            print(f"Board ID {board_id}: Failed to retrieve data (status code: {response.status_code})")

    return names

def filter_financial_names(names):
    financial_terms = [
        "prodej", "veřejná zakázka", "pronájem", "akcie", "peníze",
        "finanční", "rozpočet", "investice", "úvěr", "půjčka", "dotace",
        "náklady", "zisk", "ztráta", "kapitál", "trh", "dividenda", "nájem"
    ]

    filtered_names = []
    for board_id, name in names:
        normalized_name = unidecode(name).upper()
        for term in financial_terms:
            if term.upper() in normalized_name:
                filtered_names.append((board_id, name))
                break
    
    return filtered_names

# Call the functions
names = get_board_names()
filtered_names = filter_financial_names(names)

# Print the filtered names
for board_id, name in filtered_names:
    print(f"Board ID: {board_id}, Název: {name}")
