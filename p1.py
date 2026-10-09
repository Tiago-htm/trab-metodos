def lerInstance(caminho):
    instancia = {'qtdVertices': None, 'qtdArestas': None,
                 's': None, 't': None, 'arestas': []}
    with open(caminho) as f:
        for texto in f:
            campos = texto.split()
            if not campos:
                continue
            tipo = campos[0]
            if tipo == 'c': 
                continue  
            elif tipo == 'p':       
                instancia['qtdVertices'] = int(campos[2])
                instancia['qtdArestas'] = int(campos[3])
            elif tipo == 'n':       
                if campos[2] == 's':
                    instancia['s'] = int(campos[1])
                elif campos[2] == 't':
                    instancia['t'] = int(campos[1])
                else:
                    raise ValueError(f'{caminho}: linha  invalida: {texto.strip()}')
            elif tipo == 'a':       
                instancia['arestas'].append((int(campos[1]), int(campos[2]), float(campos[3])))
    return instancia

def montarPlCorte(instancia):
    arestas = instancia['arestas']
    qtdArestas = len(arestas)
    qtdVertices = instancia['qtdVertices']
    s = instancia['s']
    t = instancia['t']

    qtdColunas = qtdArestas + qtdVertices

    A = []
    b = []
    for indexAresta, (u, v, cap) in enumerate(arestas):
        coef1 = [0.0] * qtdColunas
        coef1[indexAresta] = -1.0                  
        coef1[qtdArestas + u - 1] = -1.0           
        coef1[qtdArestas + v - 1] = 1.0             
        A.append(coef1)
        b.append(0.0)

    coef_s1 = [0.0] * qtdColunas
    coef_s1[qtdArestas + s - 1] = 1.0
    A.append(coef_s1)
    b.append(0.0)

    coef_s2 = [0.0] * qtdColunas
    coef_s2[qtdArestas + s - 1] = -1.0
    A.append(coef_s2)
    b.append(0.0)

    coef_t1 = [0.0] * qtdColunas
    coef_t1[qtdArestas + t - 1] = 1.0
    A.append(coef_t1)
    b.append(1.0)

    coef_t2 = [0.0] * qtdColunas
    coef_t2[qtdArestas + t - 1] = -1.0
    A.append(coef_t2)
    b.append(-1.0)

    c = [0.0] * qtdColunas
    for indexAresta, (u, v, cap) in enumerate(arestas):
        c[indexAresta] = cap 
    

    return {'A': A, 'b': b, 'c': c}


if __name__ == '__main__':
    instancia = lerInstance('p1/instance1.min')
    print('qtdVertices =', instancia['qtdVertices'],
          '| s =', instancia['s'], '| t =', instancia['t'])
    print('arestas =', instancia['arestas'])
    pl = montarPlCorte(instancia)
    for linha, bi in zip(pl['A'], pl['b']):
        print(linha, '<=', bi)
    print('c =', pl['c'])