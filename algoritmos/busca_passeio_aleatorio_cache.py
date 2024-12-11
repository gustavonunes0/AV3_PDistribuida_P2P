import random
import json

def atualizar_cache_no_json(arquivo_json, cache):
    """Atualiza a parte de cache do JSON com os novos dados"""
    with open(arquivo_json, 'r+') as f:
        dados = json.load(f)
        dados['cache'] = cache  # Atualiza a seção do cache com os dados modificados
        f.seek(0)  # Volta para o início do arquivo
        json.dump(dados, f, indent=2)  # Escreve de volta no arquivo

def busca_passeio_aleatorio_cache(grafo, no_inicial, recurso, ttl, config, cache, arquivo_json):
    visitados = set()
    mensagens = 0
    arestas_percorridas = []  # Lista para armazenar as arestas percorridas
    no_atual = no_inicial

    while ttl >= 0:
        visitados.add(no_atual)

        cache_atual = cache.get(no_atual, [])
        # Verificar se o recurso está no cache do nó atual
        if any(dicionario.get(recurso) is not None for dicionario in cache_atual):
            print(f"Recurso '{recurso}' encontrado no cache do nó {no_atual}.")
            return visitados, mensagens, arestas_percorridas, True

        mensagens += 1
        if recurso in config['resources'].get(no_atual, []):
            if {recurso: no_atual} not in cache.get(no_inicial, []):
                cache.setdefault(no_inicial, []).append({recurso: no_atual}) 
            print(f"Recurso '{recurso}' encontrado diretamente no nó {no_atual}.")
            atualizar_cache_no_json(arquivo_json, cache)
            return visitados, mensagens, arestas_percorridas, True
        

        vizinhos = list(grafo.neighbors(no_atual))
        proximo_no = random.choice(vizinhos)
        while(proximo_no in visitados and len(vizinhos) > 0):
            vizinhos.remove(proximo_no)
            if(len(vizinhos) > 0):
                proximo_no = random.choice(vizinhos)
       
        # if(len(vizinhos) == 0 and len() != len(visitados)):
        #     proximo_no = random.choice(vizinhos)
        
        ttl -= 1
        if(ttl >= 0):
            arestas_percorridas.append((no_atual, proximo_no))  # Armazena a aresta
            no_atual = proximo_no

    return visitados, mensagens, arestas_percorridas, False
