import csv
import json
from tqdm import tqdm

def csv_para_json(csv_file, json_file):
    dados = []

    with open(csv_file, mode='r', encoding='utf-8') as file_csv:
        csv_reader = csv.DictReader(file_csv, delimiter=';')
        for line in csv_reader:
            dados.append(line)

    with open(json_file, mode='w', encoding='utf-8') as file_json:
        json.dump(dados, file_json, indent=4, ensure_ascii=False)


def csv_to_json_object(csv_file):
    dados = []

    with open(csv_file, mode='r', encoding='utf-8-sig') as file_csv:
        csv_reader = csv.DictReader(file_csv, delimiter=';')
        for linha in tqdm(csv_reader, desc="Lendo Arquivo", unit="linha"):
            dados.append(linha)
    return dados
