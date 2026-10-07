import numpy as np
np.set_printoptions(linewidth=150, formatter={'float': '{: 5.1f}'.format})

def arestas_para_matriz(arestas, qtdVertices):
    matriz = np.zeros((qtdVertices, qtdVertices))
    for u, v, peso in arestas:
        matriz[u-1][v-1] = peso
        matriz[v-1][u-1] = peso
    return matriz