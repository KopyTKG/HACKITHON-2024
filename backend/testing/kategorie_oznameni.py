import re

import psycopg2
from unidecode import unidecode

conn = psycopg2.connect("dbname=postgres user=postgres host=viaduct.proxy.rlwy.net port=51943 password=BeicfkeCYmrolGsYgFOXkUawuesjkcYt")
cur = conn.cursor()
cur.execute("SELECT * FROM public.oznameni")
rows = cur.fetchall()

output_file = 'financial_names.txt'


def filter_oznameni(name):
    financial_terms = [
        "oznameni"
    ]

    normalized_name = unidecode(name).upper()
    for term in financial_terms:
        if term.upper() in normalized_name:
            return True
    return False


def filter_rozhodnuti(name):
    financial_terms = [
        "rozhodnuti"
    ]

    normalized_name = unidecode(name).upper()
    for term in financial_terms:
        if term.upper() in normalized_name:
            return True
    return False


def filter_stanoveni(name):
    financial_terms = [
        "stanoveni"
    ]

    normalized_name = unidecode(name).upper()
    for term in financial_terms:
        if term.upper() in normalized_name:
            return True
    return False



def filter_vyhlaska(name):
    financial_terms = [
        "vyhlask"
    ]

    normalized_name = unidecode(name)
    pattern = re.compile('|'.join(financial_terms), re.IGNORECASE)

    if pattern.search(normalized_name):
        return True
    return False

def filter_drazba(name):
    financial_terms = [
        "draz"
    ]

    normalized_name = unidecode(name)
    pattern = re.compile('|'.join(financial_terms), re.IGNORECASE)

    if pattern.search(normalized_name):
        return True
    return False


def filter_rozpocet(name):
    financial_terms = [
        "rozpoc"
    ]

    normalized_name = unidecode(name)
    pattern = re.compile('|'.join(financial_terms), re.IGNORECASE)

    if pattern.search(normalized_name):
        return True
    return False

def filter_prodej(name):
    financial_terms = [
        "prodej"
    ]

    normalized_name = unidecode(name)
    pattern = re.compile('|'.join(financial_terms), re.IGNORECASE)

    if pattern.search(normalized_name):
        return True
    return False


def filter_nalezy(name):
    financial_terms = [
        "nalez"
    ]

    normalized_name = unidecode(name)
    pattern = re.compile('|'.join(financial_terms), re.IGNORECASE)

    if pattern.search(normalized_name):
        return True
    return False


def filter_stavba(name):
    financial_terms = [
        "stavb", "ulic", "revitalizace"
    ]

    normalized_name = unidecode(name)
    pattern = re.compile('|'.join(financial_terms), re.IGNORECASE)

    if pattern.search(normalized_name):
        return True
    return False


def filter_dodavky(name):
    financial_terms = [
        "dodavk", "preruseni" , "pitne vody", "elektrin"
    ]
    normalized_name = unidecode(name)
    pattern = re.compile('|'.join(financial_terms), re.IGNORECASE)

    if pattern.search(normalized_name):
        return True
    return False


with open(output_file, 'w', encoding='utf-8') as file:

    for row in rows:
        file.write('')
        oznameni = filter_oznameni(row[1])
        if oznameni:
            file.write(f'(1, {row[0]}),\n')

        rozhodnuti = filter_rozhodnuti(row[1])
        if rozhodnuti:
            file.write(f'(2, {row[0]}),\n')

        stanoveni = filter_stanoveni(row[1])
        if stanoveni:
            file.write(f'(3, {row[0]}),\n')

        vyhlaska = filter_vyhlaska(row[1])
        if vyhlaska:
            file.write(f'(4, {row[0]}),\n')

        drazba = filter_drazba(row[1])
        if drazba:
            file.write(f'(5, {row[0]}),\n')

        rozpocet = filter_rozpocet(row[1])
        if rozpocet:
            file.write(f'(6, {row[0]}),\n')

        prodej = filter_prodej(row[1])
        if prodej:
            file.write(f'(7, {row[0]}),\n')

        nalezy = filter_nalezy(row[1])
        if nalezy:
            file.write(f'(8, {row[0]}),\n')

        stavba = filter_stavba(row[1])
        if stavba:
            file.write(f'(9, {row[0]}),\n')

        dodavky = filter_dodavky(row[1])
        if dodavky:
            file.write(f'(10, {row[0]}), \n')

