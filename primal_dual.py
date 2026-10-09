
# c Minimum s-t cut instance 1
# c 10 vertices, source=1, sink=10
# p min 10 14
# n 1 s
# n 10 t
# a 1 2 10
# a 1 3 8
# a 2 4 5
# a 2 5 7
# a 3 4 6
# a 3 6 9
# a 4 7 4
# a 5 7 8
# a 5 8 6
# a 6 8 5
# a 6 9 7
# a 7 10 10
# a 8 10 8
# a 9 10 6


def primalDual(tableau):
    #a base é quantidade de restrições que existem!!
    quantidadeR = tableau.shape[0] -1
    quantidadeColuna = tableau.shape[1]
    #
    inicioFolga =  quantidadeColuna - quantidadeR -1
    base = list(range(inicioFolga, inicioFolga+quantidadeR))
    while True:
      linhaRetirada = None
      menorValor = 0
      for i, valor in enumerate(tableau[:-1, -1]):
            if valor < 0:
                if menorValor > valor:
                    menorValor, linhaRetirada = valor, i
      if linhaRetirada is None:
            print("Interacao acabou")
            break
      colunaEntra = None
      melhorRazao = -100000000000000

      for  j, valor in enumerate(tableau[linhaRetirada, :-1]):
            if valor < 0:
                razao = tableau[-1, j] / valor  
                if razao >  melhorRazao:
                     melhorRazao, colunaEntra = razao, j
      if colunaEntra is None:
            print("PPL sem solucao")
            break
      pivo = tableau[linhaRetirada, colunaEntra]
      tableau[linhaRetirada] = tableau[linhaRetirada] / pivo
      #print(tableau[linhaRetirada])
      for k  in range(tableau.shape[0]):
            if k  != linhaRetirada:
                  novaEntrada = tableau[k,colunaEntra]
                  tableau[k] = tableau[k] - novaEntrada * tableau[linhaRetirada]
      base[linhaRetirada] = colunaEntra
     
    while True: 
         colunaEntra = None
         menorValor = 0
         for j, valor in enumerate(tableau[-1, :-1]):
            if valor < -1e-9:
                  if menorValor > valor:
                        menorValor, colunaEntra =  valor, j
         if colunaEntra is None:
            break 
         linhaRetirada = None
         melhorRazao =  10000000000000000000
         for i, valor in enumerate(tableau[:-1,colunaEntra]):
             if valor > 1e-9:
                  razao = tableau[i,-1] / valor
                  if razao < melhorRazao:
                        melhorRazao, linhaRetirada =  razao, i
         if linhaRetirada is None:
            print("PPL ilimitado")
            break
         pivo = tableau[linhaRetirada, colunaEntra]
         tableau[linhaRetirada] = tableau[linhaRetirada] / pivo
         for k in range(tableau.shape[0]):
            if k != linhaRetirada:
                novaEntrada = tableau[k, colunaEntra]
                tableau[k] = tableau[k] - novaEntrada * tableau[linhaRetirada]
         base[linhaRetirada] = colunaEntra


    return tableau, base


def corteMinimo(tableau, quantidadeVertice, quantidadeAresta):
    corteS = []
    corteT = []
    tableau, base  = primalDual(tableau)

    num_vars = quantidadeAresta + quantidadeVertice
    num_restricoes = tableau.shape[0] - 1
    
    primais_ativas = {}
    for coluna in range(num_vars):
        if coluna in base:
            valor = round(tableau[base.index(coluna), -1], 5)
            if valor > 0:
                if coluna < quantidadeAresta:
                    primais_ativas[f"x_aresta_{coluna}"] = valor
                else:
                    primais_ativas[f"d_vertice_{coluna - quantidadeAresta + 1}"] = valor
    
    for coluna in range(quantidadeAresta, quantidadeAresta + quantidadeVertice):
      valor = 0
      if coluna in base:
        valor = tableau[base.index(coluna),-1]
      vertice =  coluna - quantidadeAresta + 1
      if round(valor) == 0:
            corteS.append(vertice)
      else:
            corteT.append(vertice)

    duais_ativas = {}
    for i in range(num_restricoes):
      coluna_slack = num_vars + i
      valor_dual = round(tableau[-1, coluna_slack], 5)
      if abs(valor_dual) > 0:
            duais_ativas[f"y_{i+1}"] = abs(valor_dual)
    W = -tableau[-1, -1]

    return W, corteS, corteT, primais_ativas, duais_ativas


def mercadoria(tableau, quantidadeAresta, quantidadeMercadoria):
    fluxos = []
    tableau, base = primalDual(tableau)
    
    num_vars = quantidadeAresta * quantidadeMercadoria
    num_restricoes = tableau.shape[0] - 1
    
    for coluna in range(num_vars):
        valor = 0
        if coluna in base:
            valor = round(tableau[base.index(coluna), -1], 5)
        if valor > 0:
            mercadoria_id = (coluna // quantidadeAresta) + 1
            aresta_id = coluna % quantidadeAresta
            fluxos.append((mercadoria_id, aresta_id, valor))

    duais_ativas = {}
    for i in range(num_restricoes):
        coluna_slack = num_vars + i
        valor_dual = round(tableau[-1, coluna_slack], 5)
        if abs(valor_dual) > 0:
            duais_ativas[f"y_{i+1}"] = abs(valor_dual)

    Z = tableau[-1, -1]

    return Z, fluxos, duais_ativas
