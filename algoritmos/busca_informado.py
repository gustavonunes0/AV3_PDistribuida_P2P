import random

def busca_informado(grafo, no_inicial, recurso, ttl, config):
    visitados = set()
    mensagens = 0
    no_atual = no_inicial

    while ttl > 0:
        if no_atual in visitados:
            break
        visitados.add(no_atual)
        mensagens += 1
        if recurso in config['resources'].get(no_atual, []):
            return visitados, mensagens, True
        vizinhos = list(grafo.neighbors(no_atual))
        if not vizinhos:
            break
        vizinhos_nao_visitados = [n for n in vizinhos if n not in visitados]
        if vizinhos_nao_visitados:
            no_atual = random.choice(vizinhos_nao_visitados)
        else:
            no_atual = random.choice(vizinhos)
        ttl -= 1
    return visitados, mensagens, False