
# metaheuristics/tabu_search.py

import random
import time
from utils import (
    calcular_custo_total,
    gerar_solucao_inicial,
    vizinhanca_swap,
    vizinhanca_relocate,
    vizinhanca_2opt,
    solucao_valida
)

def tabu_search(
    dados,
    tempo_limite=1800,
    intensificacao=True,
    diversificacao=True,
    tamanho_tabu=5,
    max_iter_sem_melhora=1
):
    """
    Tabu Search para o CVRP.
    - dados: dicionário com informações da instância (coordenadas, demandas, capacidade, etc)
    - tempo_limite: tempo máximo de execução (segundos)
    - intensificacao: ativa busca local agressiva
    - diversificacao: ativa reinicializações periódicas
    - tamanho_tabu: tamanho da lista tabu
    - max_iter_sem_melhora: critério de parada secundário
    Retorna a melhor solução encontrada (lista de rotas).
    """
    inicio = time.time()
    melhor_solucao = gerar_solucao_inicial(dados)
    melhor_custo = calcular_custo_total(melhor_solucao, dados)
    solucao_atual = [rota[:] for rota in melhor_solucao]
    custo_atual = melhor_custo

    lista_tabu = []
    iter_sem_melhora = 0
    iter_total = 0

    while (time.time() - inicio) < tempo_limite and iter_sem_melhora < max_iter_sem_melhora:
        vizinhos = []
        # Geração de vizinhança: swap, relocate, 2-opt
        vizinhos += vizinhanca_swap(solucao_atual, dados)
        vizinhos += vizinhanca_relocate(solucao_atual, dados)
        if intensificacao:
            vizinhos += vizinhanca_2opt(solucao_atual, dados)
        # Avalia vizinhos e aplica lista tabu
        melhor_vizinho = None
        melhor_vizinho_custo = float('inf')
        movimento_escolhido = None
        for vizinho, movimento in vizinhos:
            if movimento in lista_tabu:
                continue
            if not solucao_valida(vizinho, dados):
                continue
            custo = calcular_custo_total(vizinho, dados)
            if custo < melhor_vizinho_custo:
                melhor_vizinho = vizinho
                melhor_vizinho_custo = custo
                movimento_escolhido = movimento
        # Se não encontrou vizinho válido, faz diversificação (se ativada)
        if melhor_vizinho is None:
            if diversificacao:
                solucao_atual = gerar_solucao_inicial(dados)
                custo_atual = calcular_custo_total(solucao_atual, dados)
                lista_tabu = []
                iter_sem_melhora += 1
                iter_total += 1
                continue
            else:
                break
        # Atualiza solução atual
        solucao_atual = [rota[:] for rota in melhor_vizinho]
        custo_atual = melhor_vizinho_custo
        lista_tabu.append(movimento_escolhido)
        if len(lista_tabu) > tamanho_tabu:
            lista_tabu.pop(0)
        # Atualiza melhor solução
        if custo_atual < melhor_custo:
            melhor_solucao = [rota[:] for rota in solucao_atual]
            melhor_custo = custo_atual
            iter_sem_melhora = 0
        else:
            iter_sem_melhora += 1
        iter_total += 1
    return melhor_solucao
