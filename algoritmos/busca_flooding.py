from collections import deque

def busca_flooding(grafo, no_inicial, recurso, ttl, config):
    visitados = set()
    mensagens = 0
    fila = deque([(no_inicial, ttl)])
    
    while fila:
        no_atual, ttl_atual = fila.popleft()
        if ttl_atual <= 0 or no_atual in visitados:
            continue
        visitados.add(no_atual)
        mensagens += 1
        if recurso in config['resources'].get(no_atual, []):
            return visitados, mensagens, True
        for vizinho in grafo.neighbors(no_atual):
            fila.append((vizinho, ttl_atual - 1))
    return visitados, mensagens, False