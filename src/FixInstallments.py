from http.client import responses

import requests
import json
# import os
import logging
from datetime import datetime, time

from twisted.python.util import println

from src.utils import RestUtils
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.utils.CsvToJson import csv_to_json_object
from src.utils.PayloadUtils import arap_update_item, arap_policy_query_payload, arap_endo_query_payload, \
    arap_update_item_to_1
from src.utils.RestUtils import  post_request
from tqdm import tqdm

host = "https://br-gw.insuremo.com/hdibrazil/1.0"
arap_query_api= host + "/bcp-bff-app/v1/bcpbff/queryArapPage"
arap_update_api= host + "/bcp-bff-app/v1/bcpbff/updateArapList"
token = "HpQlzpc1SzOp9nEFRH-2NA"
headers = {'Content-Type': 'application/json', 'x-mo-tenant-code': 'hdibrazil', 'Authorization': 'Bearer ' + token}


def processar_item(item):
    response = query_arap(item["cancelar"], item["tipo"])
    arap_list = []
    if response["TotalElements"] > 0:
        for element in response["ElementsInCurrentPage"]:
            logging.debug("Id => {}, No => {} ".format(element['ArapId'], element['ArapNo']))
            arap_list.append(arap_update_item_to_1(element['ArapId'], element['ArapNo']))

        response = cancelar_pagamento(arap_list)


def run_in_threads(lista):
    resultados = []
    with ThreadPoolExecutor(max_workers=15) as executor:
        # Submete as tarefas ao pool de threads
        futures = {executor.submit(processar_item, item): item for item in lista}

        # Usa tqdm para exibir a barra de progresso
        for future in tqdm(as_completed(futures), total=len(lista), desc="Concelando parcelas", unit="item"):
            resultados.append(future.result())
    return resultados

def cancelar_pagamento(arap_list):
    response = post_request(url=arap_update_api, json=arap_list, headers=headers)
    return  response.json()





def query_arap(business_no, type):
    payload = {}
    if type == "endo":
        payload = arap_endo_query_payload(business_no)
    elif type == "policy":
        payload = arap_policy_query_payload(business_no)

    response = post_request(url = arap_query_api, json= payload , headers= headers)
    return response.json()


# def process(data):
#     # for item in data:
#     for item in tqdm(data, desc="Cancelando pagamentos", unit="item"):
#         response = query_arap(item["cancelar"])
        # print(response.json())


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
    content =  csv_to_json_object('data/cancelar-20250512-001.csv')
    # println(content)
    #process(content)
    run_in_threads(content)

if __name__ == '__main__':
    try:
        start()
    except:
        print("main error...")
    finally:
        print('Finish')