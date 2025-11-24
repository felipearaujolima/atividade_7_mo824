
# heuristics/route_first.py

from utils import calcular_distancia, solucao_valida

def route_first_cluster_second(dados):
    """
    Heurística route-first, cluster-second para o CVRP.
    Retorna lista de rotas (cada rota é uma lista de índices de clientes).
    """
    coordenadas = dados['coordenadas']
    demandas = dados['demandas']
    capacidade = dados['capacidade']
    n_clientes = dados['n_clientes']
    deposito = dados['deposito']

    # Passo 1: Construir uma rota única (TSP) usando nearest neighbor
    clientes = set(range(1, n_clientes + 1))
    rota_tsp = []
    atual = deposito
    clientes_restantes = clientes.copy()
    while clientes_restantes:
        proximo = min(clientes_restantes, key=lambda i: calcular_distancia(atual, i, coordenadas))
        rota_tsp.append(proximo)
        clientes_restantes.remove(proximo)
        atual = proximo

    # Passo 2: Dividir a rota TSP em rotas viáveis (cluster-second)
    rotas = []
    carga = 0
    rota_atual = []
    for cliente in rota_tsp:
        if carga + demandas[cliente] > capacidade:
            rotas.append(rota_atual)
            rota_atual = []
            carga = 0
        rota_atual.append(cliente)
        carga += demandas[cliente]
    if rota_atual:
        rotas.append(rota_atual)

    # Verifica validade final
    if not solucao_valida(rotas, dados):
        # Se não for válida, retorna rotas individuais
        rotas = [[i] for i in range(1, n_clientes + 1)]
    return rotas
