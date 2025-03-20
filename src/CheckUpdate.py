from http.client import responses

import requests
import json
import logging
# import os
from datetime import datetime, time

from twisted.python.util import println

from src.utils import RestUtils
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.utils.CsvToJson import csv_to_json_object
from src.utils.PayloadUtils import arap_update_item, arap_policy_query_payload, arap_endo_query_payload
from src.utils.RestUtils import  post_request
from tqdm import tqdm

host = "https://br-gw.insuremo.com/hdibrazil/1.0"
arap_query_api= host + "/bcp-bff-app/v1/bcpbff/queryArapPage"
arap_update_api= host + "/bcp-bff-app/v1/bcpbff/updateArapList"
token = "s-8-sERmR0Kxtj6dVjnQmw"
headers = {'Content-Type': 'application/json', 'x-mo-tenant-code': 'hdibrazil', 'Authorization': 'Bearer ' + token}




def check_update(item):
    response = query_arap(item["cancelar"], item["tipo"])
    if response["TotalElements"] > 0:
        logging.warning("Item: {0}, TotalElements: {1}", item["cancelar"], response["TotalElements"])


def run_in_threads(lista):
    resultados = []
    with ThreadPoolExecutor(max_workers=30) as executor:
        # Submete as tarefas ao pool de threads
        futures = {executor.submit(check_update, item): item for item in lista}

        # Usa tqdm para exibir a barra de progresso
        for future in tqdm(as_completed(futures), total=len(lista), desc="Concelando parcelas", unit="item"):
            resultados.append(future.result())
    return resultados


def logger():
    #format = "%(asctime)s: %(message)s"
    now = datetime.now()

    logging.basicConfig(
        filename='logfile{0}.log'.format(now.strftime("%Y%m%d_%H%M%S")),  # Name of the log file
        level=logging.DEBUG,  # Set the minimum logging level
        format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
        #datefmt="%H:%M:%S"
    )


def query_arap(business_no, type):
    payload = {}
    if type == "endo":
        payload = arap_endo_query_payload(business_no)
    elif type == "policy":
        payload = arap_policy_query_payload(business_no)

    response = post_request(url = arap_query_api, json= payload , headers= headers)
    return response.json()





def start():
    logger()
    content =  csv_to_json_object('data/cancelar-20250317-001.csv')
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