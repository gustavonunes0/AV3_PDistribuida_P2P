from rede import carregar_configuracao, construir_rede
from algoritmos import busca_flooding, busca_passeio_aleatorio, busca_informado

if __name__ == "__main__":
    ARQUIVO_CONFIGURACAO = "network_config.json"
    config = carregar_configuracao(ARQUIVO_CONFIGURACAO)

    grafo = construir_rede(config)

    no_inicial = "n1"  
    recurso = "r15"  
    ttl = 5          
    algoritmo = "busca_informado" 

    if algoritmo == "busca_flooding":
        visitados, mensagens, encontrado = busca_flooding(grafo, no_inicial, recurso, ttl, config)
    elif algoritmo == "busca_passeio_aleatorio":
        visitados, mensagens, encontrado = busca_passeio_aleatorio(grafo, no_inicial, recurso, ttl, config)
    elif algoritmo == "busca_informado":
        visitados, mensagens, encontrado = busca_informado(grafo, no_inicial, recurso, ttl, config)
    else:
        raise ValueError(f"Algoritmo de busca {algoritmo} não suportado!")

    print(f"Algoritmo: {algoritmo}")
    print(f"Nó inicial: {no_inicial}")
    print(f"Recurso buscado: {recurso}")
    print(f"TTL: {ttl}")
    print(f"Mensagens trocadas: {mensagens}")
    print(f"Nós visitados: {visitados}")
    print(f"Recurso encontrado: {'Sim' if encontrado else 'Não'}")