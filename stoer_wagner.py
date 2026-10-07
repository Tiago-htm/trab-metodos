#Implementação do algoritmo de Stoer-Wagner

import numpy as np

def stoer_wagner(matriz):
    grafo = [linha[:] for linha in matriz]
    n = len(matriz)
    vertices_ativos = list(range(n))
    menor_corte = float('inf')

    particoes = [[i] for i in range(n)]
    melhor_particao = []

    while len(vertices_ativos) > 1:
        #Fase de busca
        A = [vertices_ativos[0]]
        pesos = {v: grafo[vertices_ativos[0]][v] for v in vertices_ativos if v != vertices_ativos[0]}

        #Busca de Adjacência Maxima
        while(len(A) < len(vertices_ativos)):
            proximo = max(pesos, key=pesos.get)
            A.append(proximo)

            for v in pesos:
                if v != proximo:
                    pesos[v] += grafo[proximo][v]

            del pesos[proximo]

        #Fase de corte
        s = A[-2]
        t = A[-1]

        corte_atual = sum(grafo[t][v] for v in vertices_ativos if v != t)

        if corte_atual < menor_corte:
            menor_corte = corte_atual
            melhor_particao = particoes[t][:]

        for v in vertices_ativos:
            if v != s and v != t:
                grafo[s][v] += grafo[t][v]
                grafo[v][s] += grafo[v][t]

        particoes[s].extend(particoes[t])
        vertices_ativos.remove(t)

    return menor_corte, melhor_particao