import requests
import logging

token_api = "https://portal.insuremo.com/cas/ebao/v2/json/tickets"


def get_request(url, headers):
    try:
        response = requests.get(url=url, headers=headers, timeout=120)
        if response.status_code == 200:
            return response
        else:
            logging.info(response.status_code)
    except requests.exceptions.HTTPError as err:
        logging.error("request error" + err)
        logging.error("request error detail" +err.response.text)

def post_request(url, json, headers):
    try:
        response = requests.post(url = url, json = json, headers = headers)
        if response.status_code == 200:
            return response
        else:
            a = response.status_code
    except requests.exceptions.HTTPError as err:
        logging.error("request error" + err)
        logging.error("request error detail" +err.response.text)

def get_token():
    headers = {'Content-Type': 'application/json', 'x-mo-tenant-code': 'hdibrazil'}
    body = {'username':'leandro.grimaldi@ebaotech.com', 'password': '#.macOS00.'}
    response =  post_request(token_api, body, headers)
    return response.json()["access_token"]

def logger():
    #format = "%(asctime)s: %(message)s"
    logging.basicConfig(
        filename='logfile.log',  # Name of the log file
        level=logging.DEBUG,  # Set the minimum logging level
        format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
        #datefmt="%H:%M:%S"
    )

