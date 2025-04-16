import requests

from src.utils.LogConfig import LoggerConfig

import requests
logger = LoggerConfig.setup_logger('rest-client')



class RestTemplate:
    def __init__(self, base_url=None, headers=None):
        self.base_url = base_url if base_url else ""
        self.headers = headers if headers else {}

    def get(self, endpoint, params=None, headers=None):
        url = self.base_url + endpoint
        try:
            response = requests.get(url, params=params, headers={**self.headers, **(headers or {})})
            response.raise_for_status()
            return response.json()  # Retorna a resposta em JSON
        except requests.RequestException as e:
            logger.error(f"Erro na requisição GET: {e}")
            return None

    def post(self, endpoint, json=None, headers=None):
        url = self.base_url + endpoint
        try:
            response = requests.post(url, json=json, headers={**self.headers, **(headers or {})})
            response.raise_for_status()
            logger.info(response.json())
            return response.json()  # Retorna a resposta em JSON
        except requests.RequestException as e:
            logger.error(f"Erro na requisição POST: {e}")
            return None