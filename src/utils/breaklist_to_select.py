# Lista simulada com 200.000 números de documentos
num_docs = [f"'{i:07}'" for i in range(1, 200001)]  # Exemplo de formatação numérica

# Tamanho de cada bloco
chunk_size = 2000

# Nome inicial dos arquivos
file_index = 1

# Função para gerar o arquivo
def write_to_file(filename, content):
    with open(filename, "w") as f:
        f.write(content)

# Dividindo a lista e escrevendo nos arquivos
for i in range(0, len(num_docs), chunk_size):
    chunk = num_docs[i:i + chunk_size]
    campos = ", ".join(chunk)
    select_query = f"select * from settlement where numdoc in ({campos});\n"
    update_query = f"update settlement set status = 'N' where numdoc in ({campos});\n"

    # Criar conteúdo do arquivo
    content = select_query + update_query

    # Gerar arquivo
    filename = f"query_file_{file_index}.sql"
    write_to_file(filename, content)

    print(f"Arquivo {filename} gerado com sucesso!")
    file_index += 1
