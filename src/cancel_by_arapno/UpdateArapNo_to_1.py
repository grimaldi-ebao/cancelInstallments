
import json
import logging
from datetime import datetime, time


from concurrent.futures import ThreadPoolExecutor, as_completed
from src.utils.PayloadUtils import arap_update_item, arap_policy_query_payload, arap_endo_query_payload, \
    arapno_query_payload, arap_update_item_to_1
from tqdm import tqdm

from src.utils.RestUtils import post_request

host = "https://br-gw.insuremo.com/hdibrazil/1.0"
arap_query_api= host + "/bcp-bff-app/v1/bcpbff/queryArapPage"
arap_update_api= host + "/bcp-bff-app/v1/bcpbff/updateArapList"
token = "rLSZO1IzRhWOoItjTiisQw"
headers = {'Content-Type': 'application/json', 'x-mo-tenant-code': 'hdibrazil', 'Authorization': 'Bearer ' + token}


def processar_item(item):
    response = query_arap(item)
    arap_list = []
    if response["TotalElements"] > 0:
        for element in response["ElementsInCurrentPage"]:
            logging.debug("Id => {}, No => {} ".format(element['ArapId'], element['ArapNo']))
            arap_list.append(arap_update_item_to_1(element['ArapId'], element['ArapNo']))

        response = cancelar_pagamento(arap_list)


def run_in_threads(lista):
    resultados = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        # Submete as tarefas ao pool de threads
        futures = {executor.submit(processar_item, item): item for item in lista}

        # Usa tqdm para exibir a barra de progresso
        for future in tqdm(as_completed(futures), total=len(lista), desc="Concelando parcelas", unit="item"):
            resultados.append(future.result())
    return resultados

def cancelar_pagamento(arap_list):
    response = post_request(url=arap_update_api, json=arap_list, headers=headers)
    return  response.json()


def run_single(lista):
    resultados = []

    for arap in tqdm(lista, desc="Atualizando ARAP to 1", unit="arap"):
        processar_item(arap)
        resultados.append(arap)

    return resultados

def cancelar_pagamento(arap_list):
    response = post_request(url=arap_update_api, json=arap_list, headers=headers)
    return  response.json()





def query_arap(business_no):
    payload = arapno_query_payload(business_no)
    response = post_request(url = arap_query_api, json= payload , headers= headers)
    return response.json()


# def process(data):
#     # for item in data:
#     for item in tqdm(data, desc="Cancelando pagamentos", unit="item"):
#         response = query_arap(item["cancelar"])
        # print(response.json())

def read_json_file(file_path):
    try:
        # Open the JSON file and load its content
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' is not in valid JSON format.")
        return None


def logger():
    #format = "%(asctime)s: %(message)s"
    now = datetime.now()

    logging.basicConfig(
        filename='logfile{0}.log'.format(now.strftime("%Y%m%d_%H%M%S")),  # Name of the log file
        level=logging.DEBUG,  # Set the minimum logging level
        format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
        #datefmt="%H:%M:%S"
    )

def start():
    logger()
    content =  read_json_file('../data/update_by_arapno.json')
    # println(content)
    #process(content)
    run_in_threads(content["cancelar"])
    # run_single(content["cancelar"])

if __name__ == '__main__':
    try:
        start()
    except:
        print("main error...")
    finally:
        print('Finish')