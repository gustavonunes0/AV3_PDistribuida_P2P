import matplotlib.pyplot as plt
from rede import carregar_configuracao, construir_rede
from algoritmos import busca_flooding, busca_passeio_aleatorio, busca_informado
import networkx as nx

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
    algoritmo = input("Algoritmo (busca_flooding, busca_passeio_aleatorio, busca_informado): ").strip()

    if algoritmo not in ["busca_flooding", "busca_passeio_aleatorio", "busca_informado"]:
        print(f"Algoritmo inválido: {algoritmo}")
        return

    config = carregar_configuracao(arquivo_configuracao)
    grafo = construir_rede(config)

    if algoritmo == "busca_flooding":
        visitados, mensagens, encontrado = busca_flooding(grafo, no_inicial, recurso, ttl, config)
    elif algoritmo == "busca_passeio_aleatorio":
        visitados, mensagens, encontrado = busca_passeio_aleatorio(grafo, no_inicial, recurso, ttl, config)
    elif algoritmo == "busca_informado":
        visitados, mensagens, encontrado = busca_informado(grafo, no_inicial, recurso, ttl, config)

    arestas_visitadas = []
    visitados = list(visitados)
    for i in range(len(visitados) - 1):
        if grafo.has_edge(visitados[i], visitados[i + 1]):
            arestas_visitadas.append((visitados[i], visitados[i + 1]))

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


if __name__ == "__main__":
    main()