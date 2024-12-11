import matplotlib.pyplot as plt
from rede import carregar_configuracao, construir_rede
from algoritmos import busca_flooding, busca_passeio_aleatorio, busca_passeio_aleatorio_cache, busca_flooding_cache
import networkx as nx
import json

def exibir_grafo(grafo, caminho=None):
    pos = nx.spring_layout(grafo)  

    nx.draw(
        grafo, pos, with_labels=True, node_color="lightblue", font_weight="bold", node_size=700
    )

    if caminho:
        nos_visitados = caminho.get("nos", set())
        arestas_visitadas = caminho.get("arestas", [])

        nx.draw_networkx_nodes(
            grafo, pos, nodelist=nos_visitados, node_color="orange", node_size=800
        )
        
        nx.draw_networkx_edges(
            grafo, pos, edgelist=arestas_visitadas, edge_color="red", width=2
        )

    plt.title("Rede P2P - Caminho Percorrido")
    plt.show()

def main():
    print("Simulação de rede P2P com algoritmos de busca.\n")

    arquivo_configuracao = "network_config.json"
    print(f"Usando arquivo de configuração: {arquivo_configuracao}\n")

    no_inicial = input("Nó inicial (ex: n1): ").strip()
    recurso = input("Recurso buscado (ex: r15): ").strip()
    ttl = int(input("Tempo de vida (TTL, ex: 5): ").strip())
    algoritmo = input("Algoritmo (busca_flooding, busca_flooding_cache, busca_passeio_aleatorio, busca_passeio_aleatorio_cache): ").strip()

    if algoritmo not in ["busca_flooding", "busca_flooding_cache", "busca_passeio_aleatorio", "busca_passeio_aleatorio_cache"]:
        print(f"Algoritmo inválido: {algoritmo}")
        return

    # Carregar configuração
    with open(arquivo_configuracao, 'r') as f:
        config = json.load(f)
    
    cache = carregar_cache(arquivo_configuracao)
    
    # Construir a rede
    grafo = nx.Graph()
    for edge in config['edges']:
        grafo.add_edge(*edge)

    # Executar o algoritmo de busca escolhido
    if algoritmo == "busca_flooding":
        visitados, mensagens, arestas_visitadas, encontrado = busca_flooding(grafo, no_inicial, recurso, ttl, config)
    elif algoritmo == "busca_flooding_cache":
        visitados, mensagens, arestas_visitadas, encontrado = busca_flooding_cache(grafo, no_inicial, recurso, ttl, config, cache, arquivo_configuracao)
    elif algoritmo == "busca_passeio_aleatorio":
        visitados, mensagens, arestas_visitadas, encontrado = busca_passeio_aleatorio(grafo, no_inicial, recurso, ttl, config)
    elif algoritmo == "busca_passeio_aleatorio_cache":
        visitados, mensagens, arestas_visitadas, encontrado = busca_passeio_aleatorio_cache(grafo, no_inicial, recurso, ttl, config, cache, arquivo_configuracao)
    
    visitados = list(visitados)

    caminho = {"nos": set(visitados), "arestas": arestas_visitadas}

    print("\nResultado da busca:")
    print(f"Algoritmo: {algoritmo}")
    print(f"Nó inicial: {no_inicial}")
    print(f"Recurso buscado: {recurso}")
    print(f"TTL: {ttl}")
    print(f"Mensagens trocadas: {mensagens}")
    print(f"Nós visitados: {visitados}")
    print(f"Recurso encontrado: {'Sim' if encontrado else 'Não'}")
    exibir_grafo(grafo, caminho)

def carregar_cache(arquivo_configuracao):
    with open(arquivo_configuracao, 'r') as f:
        config = json.load(f)
    
    cache = config.get('cache', {})

    return cache

if __name__ == "__main__":
    main()
