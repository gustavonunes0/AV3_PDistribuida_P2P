import json
from collections import deque

def atualizar_cache_no_json(arquivo_json, cache):
    """Atualiza a parte de cache do JSON com os novos dados"""
    with open(arquivo_json, 'r+') as f:
        dados = json.load(f)
        dados['cache'] = cache  # Atualiza a seção do cache com os dados modificados
        f.seek(0)  # Volta para o início do arquivo
        json.dump(dados, f, indent=2)  # Escreve de volta no arquivo

def busca_flooding_cache(grafo, no_inicial, recurso, ttl, config, cache, arquivo_json):
    visitados = set()
    mensagens = 0
    arestas_percorridas = []
    fila = deque([(no_inicial, ttl)])
    achou = False

    while fila:
        no_atual, ttl_atual = fila.popleft()

        if ttl_atual < 0 or no_atual in visitados:
            continue

        visitados.add(no_atual)

        cache_atual = cache.get(no_atual, [])
        # Verificar se o recurso está no cache do nó atual
        if any(dicionario.get(recurso) is not None for dicionario in cache_atual):
            print(f"Recurso '{recurso}' encontrado no cache do nó {no_atual}.")
            return visitados, mensagens, arestas_percorridas, True
        
        mensagens += 1
        # Verificar se o recurso está diretamente disponível no nó atual
        if recurso in config['resources'].get(no_atual, []):
            # Atualizar o cache de todos os nós visitados com a localização do recurso

            if {recurso: no_atual} not in cache.get(no_inicial, []):  # Verifica se o recurso já está no cache do nó
                cache.setdefault(no_inicial, []).append({recurso: no_atual})  # Inicializa a lista e adiciona o recurso
            print(f"Recurso '{recurso}' encontrado diretamente no nó {no_atual}.")
            
            # Atualizar o cache no arquivo JSON
            atualizar_cache_no_json(arquivo_json, cache)
            achou = True

        # Propagar a busca para os vizinhos
        for vizinho in grafo.neighbors(no_atual):
            if vizinho not in visitados and ttl_atual > 0:
                fila.append((vizinho, ttl_atual - 1))
                arestas_percorridas.append((no_atual, vizinho))

    print(f"Recurso '{recurso}' não encontrado.")
    return visitados, mensagens, arestas_percorridas, achou
