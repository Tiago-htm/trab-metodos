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
    qtdAresta = len(arestas)
    s = instancia['s']
    t = instancia['t']

    A = []
    b = []
    for indexAresta, (u, v, cap) in enumerate(arestas):
        coef = [0.0] * qtdAresta
        coef[indexAresta] = 1.0
        A.append(coef)
        b.append(cap)
    for vertice in range(1, instancia['qtdVertices'] + 1):
        if vertice == s or vertice == t:
            continue
        coef = [0.0] * qtdAresta
        for indexAresta, (u, v, cap) in enumerate(arestas):
            if v == vertice:
                coef[indexAresta] += 1.0
            if u == vertice:
                coef[indexAresta] -= 1.0
        A.append(coef)
        b.append(0.0)
        A.append([-x for x in coef])
        b.append(0.0)
    c = [0.0] * qtdAresta
    for indexAresta, (u, v, cap) in enumerate(arestas):
        if v == t:
            c[indexAresta] = 1.0

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