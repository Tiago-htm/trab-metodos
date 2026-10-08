import numpy as np
np.set_printoptions(linewidth=150, formatter={'float': '{: 5.1f}'.format})

def arestas_para_matriz(arestas, qtdVertices):
    matriz = np.zeros((qtdVertices, qtdVertices))
    for u, v, peso in arestas:
        matriz[u-1][v-1] = peso
        matriz[v-1][u-1] = peso
    return matriz

def montar_tableau(pl, objetivo):
    A = np.array(pl['A'])
    b = np.array(pl['b'])
    c = np.array(pl['c'])
    
    num_restricoes, num_variaveis = A.shape
    
    matriz_folga = np.eye(num_restricoes)
    
    corpo_tableau = np.hstack((A, matriz_folga))
    
    b_coluna = b.reshape(-1, 1)
    corpo_tableau = np.hstack((corpo_tableau, b_coluna))
    
    linha_z = np.zeros(num_variaveis + num_restricoes + 1)

    if objetivo == 'max':
        linha_z[:num_variaveis] = -c
    elif objetivo == 'min':
        linha_z[:num_variaveis] = c
    
    tableau = np.vstack((corpo_tableau, linha_z))
    
    return tableau