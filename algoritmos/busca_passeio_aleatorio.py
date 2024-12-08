import random

def busca_passeio_aleatorio(grafo, no_inicial, recurso, ttl, config):
    visitados = set()
    mensagens = 0
    arestas_percorridas = []  # Lista para armazenar as arestas percorridas
    no_atual = no_inicial

    while ttl > 0:
        if no_atual in visitados:
            continue
        visitados.add(no_atual)
        mensagens += 1
        if recurso in config['resources'].get(no_atual, []):
            return visitados, mensagens, arestas_percorridas, True
        vizinhos = list(grafo.neighbors(no_atual))
        if not vizinhos:
            break
        proximo_no = random.choice(vizinhos)
        arestas_percorridas.append((no_atual, proximo_no))  # Armazena a aresta
        no_atual = proximo_no
        ttl -= 1

    return visitados, mensagens, arestas_percorridas, False
