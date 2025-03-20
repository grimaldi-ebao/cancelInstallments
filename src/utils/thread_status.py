from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def processar_item(item):
    # Função de processamento de cada item (substitua com sua lógica)
    return f"Processado: {item}"

def processar_lista_com_threads(lista):
    resultados = []
    with ThreadPoolExecutor(max_workers=25) as executor:
        # Submete as tarefas ao pool de threads
        futuros = {executor.submit(processar_item, item): item for item in lista}

        # Usa tqdm para exibir a barra de progresso
        for futuro in tqdm(as_completed(futuros), total=len(lista), desc="Processando itens", unit="item"):
            resultados.append(futuro.result())
    return resultados

# Exemplo de lista de strings
lista_strings = [f"string_{i}" for i in range(100)]  # Exemplo de 100 strings

# Processa a lista
resultados = processar_lista_com_threads(lista_strings)

# Exibe os resultados (se necessário)
print("Processamento concluído.")
