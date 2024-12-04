import json
import networkx as nx

def carregar_configuracao(arquivo):
    with open(arquivo, 'r') as f:
        return json.load(f)

def validar_rede(configuracao, grafo):
    if not nx.is_connected(grafo):
        raise ValueError("A rede não está conectada!")

    for no in grafo.nodes:
        vizinhos = len(list(grafo.neighbors(no)))
        if vizinhos < configuracao['min_neighbors'] or vizinhos > configuracao['max_neighbors']:
            raise ValueError(f"Nó {no} fora dos limites de vizinhos!")

    for no in grafo.nodes:
        if no not in configuracao['resources']:
            raise ValueError(f"Nó {no} não possui recursos!")

    if any(grafo.has_edge(no, no) for no in grafo.nodes):
        raise ValueError(f"Nó {no} não pode ter laço consigo mesmo!")

def construir_rede(configuracao):
    grafo = nx.Graph()
    grafo.add_nodes_from(configuracao['resources'].keys())
    grafo.add_edges_from(configuracao['edges'])
    validar_rede(configuracao, grafo)
    return grafo