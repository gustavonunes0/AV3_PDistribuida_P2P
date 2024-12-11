import random

def busca_passeio_aleatorio(grafo, no_inicial, recurso, ttl, config):
    visitados = set()
    mensagens = 0
    arestas_percorridas = []  # Lista para armazenar as arestas percorridas
    no_atual = no_inicial

    while ttl >= 0:
        visitados.add(no_atual)
        mensagens += 1
        if recurso in config['resources'].get(no_atual, []):
            return visitados, mensagens, arestas_percorridas, True
        vizinhos = list(grafo.neighbors(no_atual))
        proximo_no = random.choice(vizinhos)
        while(proximo_no in visitados and len(vizinhos) > 0):
            vizinhos.remove(proximo_no)
            if(len(vizinhos) > 0):
                proximo_no = random.choice(vizinhos)
        
        ttl -= 1
        if(ttl >= 0):
            arestas_percorridas.append((no_atual, proximo_no))  # Armazena a aresta
            no_atual = proximo_no

    return visitados, mensagens, arestas_percorridas, False
