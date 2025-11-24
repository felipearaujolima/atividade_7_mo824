
# heuristics/savings.py

from utils import calcular_distancia, solucao_valida

def savings_heuristica(dados):
    """
    Implementação da heurística de Savings (Clarke & Wright) para CVRP.
    Retorna lista de rotas (cada rota é uma lista de índices de clientes).
    """
    coordenadas = dados['coordenadas']
    demandas = dados['demandas']
    capacidade = dados['capacidade']
    n_clientes = dados['n_clientes']
    deposito = dados['deposito']

    # Inicialmente, cada cliente é atendido por uma rota individual
    rotas = {i: [deposito, i, deposito] for i in range(1, n_clientes + 1)}
    cargas = {i: demandas[i] for i in range(1, n_clientes + 1)}

    # Calcula savings para todos pares de clientes
    savings = []
    for i in range(1, n_clientes + 1):
        for j in range(i + 1, n_clientes + 1):
            s = (calcular_distancia(deposito, i, coordenadas) +
                 calcular_distancia(deposito, j, coordenadas) -
                 calcular_distancia(i, j, coordenadas))
            savings.append((s, i, j))
    # Ordena savings em ordem decrescente
    savings.sort(reverse=True)

    # Merge de rotas baseado nos savings
    for s, i, j in savings:
        rota_i = rotas.get(i)
        rota_j = rotas.get(j)
        if rota_i is None or rota_j is None or rota_i == rota_j:
            continue
        # Só pode unir se i está no final de uma rota e j no início de outra
        if rota_i[-2] == i and rota_j[1] == j:
            carga_total = cargas[i] + cargas[j]
            # Verifica capacidade
            if carga_total <= capacidade:
                # Une as rotas
                nova_rota = rota_i[:-1] + rota_j[1:]
                # Atualiza rotas e cargas
                for cliente in nova_rota[1:-1]:
                    rotas[cliente] = nova_rota
                cargas[nova_rota[1]] = carga_total
                cargas[nova_rota[-2]] = carga_total
    # Extrai rotas únicas
    rotas_unicas = []
    vistas = set()
    for rota in rotas.values():
        rota_tuple = tuple(rota)
        if rota_tuple not in vistas:
            # Remove depósito dos extremos para compatibilidade
            rotas_unicas.append(rota[1:-1])
            vistas.add(rota_tuple)
    # Verifica validade final
    if not solucao_valida(rotas_unicas, dados):
        # Se não for válida, retorna rotas individuais
        rotas_unicas = [[i] for i in range(1, n_clientes + 1)]
    return rotas_unicas
