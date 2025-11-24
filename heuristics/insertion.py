
# heuristics/insertion.py

from utils import calcular_distancia, solucao_valida

def insertion_heuristica(dados):
    """
    Heurística de inserção sequencial para o CVRP.
    Retorna lista de rotas (cada rota é uma lista de índices de clientes).
    """
    coordenadas = dados['coordenadas']
    demandas = dados['demandas']
    capacidade = dados['capacidade']
    n_clientes = dados['n_clientes']
    deposito = dados['deposito']

    clientes = set(range(1, n_clientes + 1))
    rotas = []
    clientes_nao_atendidos = clientes.copy()

    while clientes_nao_atendidos:
        rota = []
        carga = 0
        # Seleciona cliente mais próximo do depósito para iniciar rota
        cliente_inicial = min(clientes_nao_atendidos,
                              key=lambda i: calcular_distancia(deposito, i, coordenadas))
        rota.append(cliente_inicial)
        carga += demandas[cliente_inicial]
        clientes_nao_atendidos.remove(cliente_inicial)

        while True:
            # Busca cliente não atendido que pode ser inserido sem exceder capacidade
            candidatos = [i for i in clientes_nao_atendidos if carga + demandas[i] <= capacidade]
            if not candidatos:
                break
            # Insere o cliente que minimiza o aumento de custo na rota
            melhor_cliente = None
            melhor_custo = float('inf')
            melhor_posicao = None
            for cliente in candidatos:
                for pos in range(len(rota) + 1):
                    rota_temp = rota[:pos] + [cliente] + rota[pos:]
                    custo = calcular_custo_rota([deposito] + rota_temp + [deposito], coordenadas)
                    if custo < melhor_custo:
                        melhor_custo = custo
                        melhor_cliente = cliente
                        melhor_posicao = pos
            if melhor_cliente is not None:
                rota.insert(melhor_posicao, melhor_cliente)
                carga += demandas[melhor_cliente]
                clientes_nao_atendidos.remove(melhor_cliente)
            else:
                break
        rotas.append(rota)
    # Verifica validade final
    if not solucao_valida(rotas, dados):
        # Se não for válida, retorna rotas individuais
        rotas = [[i] for i in range(1, n_clientes + 1)]
    return rotas

def calcular_custo_rota(rota, coordenadas):
    custo = 0.0
    for i in range(len(rota) - 1):
        custo += calcular_distancia(rota[i], rota[i+1], coordenadas)
    return custo
