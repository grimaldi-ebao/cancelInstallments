import requests
import random
from concurrent.futures import ThreadPoolExecutor

# Definição dos payloads
payloads = [
    {"PolicyNo": "065722023001109930000532"},
    {"PolicyNo": "065722023001109930000534"},
    {"PolicyNo": "065722023023109930000090"}
]

# Definição dos headers
headers = {
    "Content-Type": "application/json",
    "Tenant_code": "hdibrazil"
}

# URL da API
url = "http://localhost:8290/v1/test/newEndoSeqNo"

def enviar_request(id_request):
    # Seleciona aleatoriamente um payload entre os definidos
    payload = random.choice(payloads)
    try:
        # Envia a requisição GET com os headers e o payload (via parâmetro json)
        response = requests.get(url, headers=headers, json=payload)
        print(f"Request {id_request}: Payload {payload} => Status {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Request {id_request}: Erro com payload {payload} => {e}")

def main():
    num_requests = 40  # Quantidade de requisições
    index = 0
    while index <= 10:
        with ThreadPoolExecutor(max_workers=num_requests) as executor:
            # Submete as 50 requisições em paralelo
            futures = [executor.submit(enviar_request, i + 1) for i in range(num_requests)]
            # Aguarda todas as tarefas finalizarem
            for future in futures:
                future.result()
        index = index + 1

if __name__ == "__main__":
    main()
