
# utils.py

import math
import random

def calcular_distancia(i, j, coordenadas):
    """
    Calcula a distância euclidiana entre os pontos i e j.
    """
    x1, y1 = coordenadas[i]
    x2, y2 = coordenadas[j]
    return math.hypot(x2 - x1, y2 - y1)

def calcular_custo_total(rotas, dados):
    """
    Soma o custo total das rotas (distância percorrida por todos os veículos).
    """
    coordenadas = dados['coordenadas']
    deposito = dados['deposito']
    custo = 0.0
    for rota in rotas:
        if not rota:
            continue
        # Rota começa e termina no depósito
        caminho = [deposito] + rota + [deposito]
        for i in range(len(caminho) - 1):
            custo += calcular_distancia(caminho[i], caminho[i+1], coordenadas)
    return custo

def solucao_valida(rotas, dados):
    """
    Verifica se a solução é válida: cada cliente atendido uma vez, capacidade respeitada.
    """
    demandas = dados['demandas']
    capacidade = dados['capacidade']
    n_clientes = dados['n_clientes']
    clientes_atendidos = set()
    for rota in rotas:
        carga = 0
        for cliente in rota:
            if cliente in clientes_atendidos:
                return False
            clientes_atendidos.add(cliente)
            carga += demandas[cliente]
        if carga > capacidade:
            return False
    # Todos clientes atendidos?
    return clientes_atendidos == set(range(1, n_clientes + 1))

def gerar_solucao_inicial(dados):
    """
    Gera uma solução inicial simples: cada cliente em uma rota separada.
    """
    n_clientes = dados['n_clientes']
    return [[i] for i in range(1, n_clientes + 1)]

# Vizinhanças para Tabu Search

def vizinhanca_swap(rotas, dados):
    """
    Gera vizinhos trocando dois clientes de rotas diferentes.
    Retorna lista de tuplas (nova_solucao, movimento).
    """
    vizinhos = []
    for i in range(len(rotas)):
        for j in range(i+1, len(rotas)):
            for a in range(len(rotas[i])):
                for b in range(len(rotas[j])):
                    nova_rotas = [r[:] for r in rotas]
                    nova_rotas[i][a], nova_rotas[j][b] = nova_rotas[j][b], nova_rotas[i][a]
                    movimento = ("swap", i, a, j, b)
                    if solucao_valida(nova_rotas, dados):
                        vizinhos.append((nova_rotas, movimento))
    return vizinhos

def vizinhanca_relocate(rotas, dados):
    """
    Gera vizinhos movendo um cliente de uma rota para outra.
    Retorna lista de tuplas (nova_solucao, movimento).
    """
    vizinhos = []
    for i in range(len(rotas)):
        for j in range(len(rotas)):
            if i == j:
                continue
            for a in range(len(rotas[i])):
                cliente = rotas[i][a]
                for b in range(len(rotas[j]) + 1):
                    nova_rotas = [r[:] for r in rotas]
                    # Remove cliente de rota i
                    nova_rotas[i].pop(a)
                    # Insere cliente em rota j na posição b
                    nova_rotas[j].insert(b, cliente)
                    movimento = ("relocate", i, a, j, b)
                    # Remove rotas vazias
                    nova_rotas = [r for r in nova_rotas if r]
                    if solucao_valida(nova_rotas, dados):
                        vizinhos.append((nova_rotas, movimento))
    return vizinhos

def vizinhanca_2opt(rotas, dados):
    """
    Gera vizinhos aplicando 2-opt em cada rota (inversão de subcaminho).
    Retorna lista de tuplas (nova_solucao, movimento).
    """
    vizinhos = []
    for i in range(len(rotas)):
        rota = rotas[i]
        n = len(rota)
        for a in range(n):
            for b in range(a+2, n+1):
                nova_rota = rota[:a] + rota[a:b][::-1] + rota[b:]
                nova_rotas = [r[:] for r in rotas]
                nova_rotas[i] = nova_rota
                movimento = ("2opt", i, a, b)
                if solucao_valida(nova_rotas, dados):
                    vizinhos.append((nova_rotas, movimento))
    return vizinhos

def avaliar_solucao(rotas, dados):
    """
    Retorna métricas para análise: custo, número de rotas, capacidade usada por rota.
    """
    demandas = dados['demandas']
    capacidade = dados['capacidade']
    custo = calcular_custo_total(rotas, dados)
    metricas = []
    for rota in rotas:
        carga = sum(demandas[c] for c in rota)
        metricas.append({
            "tamanho_rota": len(rota),
            "carga_rota": carga,
            "capacidade": capacidade
        })
    return {
        "custo_total": custo,
        "num_rotas": len(rotas),
        "metricas_rotas": metricas
    }
