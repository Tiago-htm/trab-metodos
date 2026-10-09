import sys
import time

from numpy import rint

import p1
import p2
import pulpTeste
import stoer_wagner as sw
import auxiliares as aux
import numpy as np
import primal_dual



if __name__ == '__main__':
    if(sys.argv[1] == "p1"):
        caminho = f"{sys.argv[1]}/instance{sys.argv[2]}.min"
        instancia = p1.lerInstance(caminho)
        pl = p1.montarPlCorte(instancia)
        matriz = aux.arestas_para_matriz(instancia['arestas'], instancia['qtdVertices'])
        
        t_inicio_pd = time.perf_counter()
        tableau_inicial = aux.montar_tableau(pl, 'min')
        W, corteS, corteT, primais_pd, duais_pd = primal_dual.corteMinimo(tableau_inicial, instancia['qtdVertices'], len(instancia['arestas']))
        t_fim_pd = time.perf_counter()
        tempo_pd = t_fim_pd - t_inicio_pd

        t_inicio_pulp = time.perf_counter()
        valor_pulp, variaveis_pulp, restricoes_pulp = pulpTeste.p1_pulp(instancia)
        t_fim_pulp = time.perf_counter()
        tempo_pulp = t_fim_pulp - t_inicio_pulp

        t_inicio_sw = time.perf_counter()
        resultado_sw = sw.stoer_wagner(matriz)
        t_fim_sw = time.perf_counter()
        tempo_sw = t_fim_sw - t_inicio_sw   

        valor_sw = resultado_sw['valor']
        particao_1_real = [v + 1 for v in resultado_sw['particao1']]
        particao_2_real = [v + 1 for v in resultado_sw['particao2']]

        print("="*60)
        print(f" RELATÓRIO: PROBLEMA 1 - CORTE MÍNIMO s-t")
        print(f" Vértices: {instancia['qtdVertices']} | Origem (s): {instancia['s']} | Destino (t): {instancia['t']}")
        print("="*60)

        print("\n[ 1. SOLUÇÃO PRIMAL-DUAL ]")
        print(f"Tempo de Execução      : {tempo_pd:.5f} segundos")
        print(f"Custo do Corte s-t (W) : {W:.2f}")
        print(f"Lado da Origem (s)     : {corteS}")
        print(f"Lado do Destino (t)    : {corteT}")
        print("\n--- Variáveis Primais (Não-Nulas) ---")
        for nome, valor in primais_pd.items():
            print(f"  {nome} = {valor}")
            
        print("\n--- Variáveis Duais (Não-Nulas) ---")
        for nome, valor in duais_pd.items():
            print(f"  {nome} = {valor}")

        print("\n[ 2. SOLUÇÃO COIN-OR (PuLP) ]")
        print(f"Tempo de Execução      : {tempo_pulp:.5f} segundos")
        print(f"Custo do Corte s-t     : {valor_pulp:.2f}")
        print("Variáveis Ativas (x_uv > 0):")
        for var in variaveis_pulp:
            val = round(var.varValue, 5) 
            if val > 0 and var.name.startswith('x'):
                print(f"  {var.name} = {val}")
        print("\n--- Variáveis Duais (Não-Nulas) ---")
        for nome_restricao, restricao in restricoes_pulp.items():
            if restricao.pi and round(restricao.pi, 5) != 0:
                print(f"  {nome_restricao} = {round(restricao.pi, 5)}")

        print("\n[ 3. CORTE MÍNIMO GLOBAL (Stoer-Wagner) ]")
        print(f"Tempo de Execução      : {tempo_sw:.5f} segundos")
        print(f"Custo do Corte Global  : {valor_sw:.2f}")
        print(f"Partição 1 : {particao_1_real}")
        print(f"Partição 2 : {particao_2_real}")

        print("\n" + "-"*60)
        print(" CONCLUSÃO DA COMPARAÇÃO:")
        if abs(W - valor_pulp) < 1e-5:
            print(" -> O Primal-Dual alcançou a mesma solução ótima do PuLP.")
        else:
            print(" -> ALERTA: Divergência entre Primal-Dual e PuLP.")
            
        if valor_sw < W:
            print(f" -> O corte global ({valor_sw}) é menor que o corte s-t ({W}).")
            print("    O elo mais fraco da rede não está na rota principal de s para t.")
        else:
            print(" -> O corte global é igual ao corte s-t. O gargalo principal separa s e t.")
        print("="*60 + "\n")


    elif(sys.argv[1] == "p2"):
        caminho = f"{sys.argv[1]}/mc_instance{sys.argv[2]}.max"
        instancia = p2.lerInstance(caminho)
        pl = p2.montarPlMercadoria(instancia)
        
        t_inicio_pd = time.perf_counter()
        tableau_inicial = aux.montar_tableau(pl, 'max')
        Z, fluxos, duais_pd = primal_dual.mercadoria(tableau_inicial, len(instancia['arestas']), instancia['qtdMercadoria'])
        t_fim_pd = time.perf_counter()
        tempo_pd = t_fim_pd - t_inicio_pd

        t_inicio_pulp = time.perf_counter()
        valor_pulp, variaveis_pulp, restricoes_pulp = pulpTeste.p2_pulp(instancia)
        t_fim_pulp = time.perf_counter()
        tempo_pulp = t_fim_pulp - t_inicio_pulp

        print("="*60)
        print(f" RELATÓRIO: PROBLEMA 2 - FLUXO MÁXIMO MULTIMERCADORIA")
        print(f" Vértices: {instancia['qtdVertice']} | Mercadorias: {instancia['qtdMercadoria']}")
        print("="*60)

        print("\n[ 1. SOLUÇÃO PRIMAL-DUAL (Seu Algoritmo) ]")
        print(f"Tempo de Execução      : {tempo_pd:.5f} segundos")
        print(f"Lucro Máximo Total (Z) : {Z:.2f}")
        print("Fluxos Ativos (f > 0):")
        for mercadoria, arco, valor in fluxos:
            u, v, cap = instancia['arestas'][arco]
            print(f"  Merc {mercadoria}: {u:2d} -> {v:2d} | Fluxo: {valor:.2f}")
        print("\n--- Variáveis Duais (Não-Nulas) ---")
        for nome, valor in duais_pd.items():
            print(f"  {nome} = {valor}")

        print("\n[ 2. SOLUÇÃO COIN-OR (PuLP) ]")
        print(f"Tempo de Execução      : {tempo_pulp:.5f} segundos")
        print(f"Lucro Máximo Total     : {valor_pulp:.2f}")
        print("Variáveis Ativas (f > 0):")
        for var in variaveis_pulp:
            val = round(var.varValue, 5) 
            if val > 0:
                print(f"  {var.name} = {val}")
        print("\n--- Variáveis Duais (Não-Nulas) ---")
        for nome_restricao, restricao in restricoes_pulp.items():
            if restricao.pi and round(restricao.pi, 5) != 0:
                print(f"  {nome_restricao} = {round(restricao.pi, 5)}")

        print("\n" + "-"*60)
        print(" CONCLUSÃO DA COMPARAÇÃO:")
        if abs(Z - valor_pulp) < 1e-5:
            print(" -> O Primal-Dual alcançou a mesma solução ótima do PuLP (Correto!).")
        else:
            print(" -> ALERTA: Divergência entre Primal-Dual e PuLP.")
        print("="*60 + "\n")