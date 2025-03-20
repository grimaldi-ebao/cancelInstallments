from tqdm import tqdm
import time  # Apenas para simular o processamento com atraso

def processar_documentos(lista_documentos):
    for documento in tqdm(lista_documentos, desc="Processando documentos", unit="documento"):
        # Simulando o processamento de cada documento (substitua por sua lógica real)
        time.sleep(0.5)  # Ajuste ou remova conforme necessário

# Exemplo de uso
lista_documentos = ["documento1.txt", "documento2.txt", "documento3.txt", "documento4.txt"]

processar_documentos(lista_documentos)