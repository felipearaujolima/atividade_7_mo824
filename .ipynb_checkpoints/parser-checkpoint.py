
# parser.py

def ler_instancia_cvrp(caminho_arquivo):
    """
    Lê uma instância CVRP no formato padrão (exemplo: X-n101-k25).
    Retorna um dicionário com coordenadas, demandas, capacidade, depósito, n_clientes.
    """
    with open(caminho_arquivo, 'r') as f:
        linhas = f.readlines()

    coordenadas = {}
    demandas = {}
    capacidade = None
    deposito = None
    n_clientes = None

    secao = None
    for linha in linhas:
        linha = linha.strip()
        if linha.startswith("CAPACITY"):
            capacidade = int(linha.split(":")[1].strip())
        elif linha.startswith("DIMENSION"):
            n_clientes = int(linha.split(":")[1].strip()) - 1  # exclui depósito
        elif linha.startswith("NODE_COORD_SECTION"):
            secao = "COORD"
            continue
        elif linha.startswith("DEMAND_SECTION"):
            secao = "DEMAND"
            continue
        elif linha.startswith("DEPOT_SECTION"):
            secao = "DEPOT"
            continue
        elif linha.startswith("EOF"):
            break
        elif secao == "COORD":
            partes = linha.split()
            if len(partes) == 3:
                idx = int(partes[0])
                x = float(partes[1])
                y = float(partes[2])
                coordenadas[idx] = (x, y)
        elif secao == "DEMAND":
            partes = linha.split()
            if len(partes) == 2:
                idx = int(partes[0])
                demanda = int(partes[1])
                demandas[idx] = demanda
        elif secao == "DEPOT":
            if linha == "-1":
                secao = None
            else:
                deposito = int(linha)

    # Se depósito não foi identificado, assume 1
    if deposito is None:
        deposito = 1

    # Se n_clientes não foi identificado, calcula pelo número de coordenadas menos depósito
    if n_clientes is None:
        n_clientes = len(coordenadas) - 1

    return {
        "coordenadas": coordenadas,   # dict: idx -> (x, y)
        "demandas": demandas,         # dict: idx -> demanda
        "capacidade": capacidade,     # int
        "deposito": deposito,         # int
        "n_clientes": n_clientes      # int (exclui depósito)
    }
