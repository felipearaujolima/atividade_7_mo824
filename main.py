
import os
import csv
import time
from multiprocessing import Pool
from parser import ler_instancia_cvrp
from heuristics.savings import savings_heuristica
from heuristics.insertion import insertion_heuristica
from heuristics.route_first import route_first_cluster_second
from metaheuristics.tabu_search import tabu_search
from utils import calcular_custo_total, avaliar_solucao

# Configurações
PASTA_INSTANCIAS = "instances"
PASTA_RESULTADOS = "resultados"
TEMPO_LIMITE = 1 * 30  # 30 minutos em segundos

HEURISTICAS = {
    "Savings": savings_heuristica,
    "Insertion": insertion_heuristica,
    "RouteFirstClusterSecond": route_first_cluster_second
}

METAHEURISTICA_CONFIGS = [
    {"nome": "TabuSearch_Simples", "intensificacao": False, "diversificacao": False},
    {"nome": "TabuSearch_Intensificacao", "intensificacao": True, "diversificacao": False},
    {"nome": "TabuSearch_Diversificacao", "intensificacao": False, "diversificacao": True},
    {"nome": "TabuSearch_Completo", "intensificacao": True, "diversificacao": True}
]

def salvar_resultados_csv(resultados, nome_csv):
    campos = [
        "Instancia", "Metodo", "Custo", "Tempo (s)", "Qtd Rotas", "Qtd Veiculos",
        "Intensificacao", "Diversificacao", "Solucao"
    ]
    existe = os.path.exists(nome_csv)
    with open(nome_csv, "a", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        if not existe:
            writer.writeheader()
        for r in resultados:
            writer.writerow(r)

def rodar_para_instancia(arquivo):
    if not os.path.exists(PASTA_RESULTADOS):
        os.makedirs(PASTA_RESULTADOS)
    resultados = []
    caminho = os.path.join(PASTA_INSTANCIAS, arquivo)
    print(f"\nProcessando instância: {arquivo}")
    dados = ler_instancia_cvrp(caminho)
    # Heurísticas construtivas
    for nome, funcao in HEURISTICAS.items():
        print(f"  Rodando heurística: {nome} ({arquivo})")
        inicio = time.time()
        solucao = funcao(dados)
        fim = time.time()
        custo = calcular_custo_total(solucao, dados)
        rotas = len(solucao)
        resultado = {
            "Instancia": arquivo,
            "Metodo": nome,
            "Custo": custo,
            "Tempo (s)": round(fim - inicio, 2),
            "Qtd Rotas": rotas,
            "Qtd Veiculos": rotas,
            "Intensificacao": "",
            "Diversificacao": "",
            "Solucao": str(solucao)
        }
        resultados.append(resultado)
        print(f"    Custo: {custo} | Tempo: {fim-inicio:.2f}s | Rotas: {rotas} ({arquivo})")
    # Metaheurística
    #for config in METAHEURISTICA_CONFIGS:
    #    print(f"  Rodando metaheurística: {config['nome']} ({arquivo})")
    #    inicio = time.time()
    #    solucao = tabu_search(
    #        dados,
    #        tempo_limite=TEMPO_LIMITE,
    #        intensificacao=config["intensificacao"],
    #        diversificacao=config["diversificacao"]
    #    )
    #    fim = time.time()
    #    custo = calcular_custo_total(solucao, dados)
    #    rotas = len(solucao)
    #    resultado = {
    #        "Instancia": arquivo,
    #        "Metodo": config["nome"],
    #        "Custo": custo,
    #        "Tempo (s)": round(fim - inicio, 2),
    #        "Qtd Rotas": rotas,
    #        "Qtd Veiculos": rotas,
    #        "Intensificacao": config["intensificacao"],
    #        "Diversificacao": config["diversificacao"],
    #        "Solucao": str(solucao)
    #    }
    #    resultados.append(resultado)
    #    print(f"    Custo: {custo} | Tempo: {fim-inicio:.2f}s | Rotas: {rotas} ({arquivo})")
    nome_csv = os.path.join(PASTA_RESULTADOS, f"resultados_{arquivo}.csv")
    salvar_resultados_csv(resultados, nome_csv)
    print(f"\nResultados salvos em {nome_csv}")

if __name__ == "__main__":
    arquivos_instancias = [f for f in os.listdir(PASTA_INSTANCIAS) if f.endswith(".vrp") or f.endswith(".txt")]
    arquivos_instancias = sorted([f for f in os.listdir(PASTA_INSTANCIAS) if f.endswith(".vrp") or f.endswith(".txt")])
    # Pool com 2 processos
    with Pool(processes=1) as pool:
        pool.map(rodar_para_instancia, arquivos_instancias)
