def lerInstance(caminho):
    instancia = {'qtdVertice': None, 'qtdAresta': None, 'qtdMercadoria': None,
                 'origens': {},    
                 'destinos': {},    
                 'premios': {},     
                 'arestas': []}
    with open(caminho) as f:
        for texto in f:
            campos = texto.split()
            if not campos:
                continue
            tipo = campos[0]
            if tipo == 'c':
                continue
            elif tipo == 'p':      
                instancia['qtdVertice'] = int(campos[2])
                instancia['qtdAresta'] = int(campos[3])
                instancia['qtdMercadoria'] = int(campos[4])
            elif tipo == 'n':       
                vertice, mercadoria = int(campos[1]), int(campos[3])
                if campos[2] == 's':
                    instancia['origens'][mercadoria] = vertice
                elif campos[2] == 't':
                    instancia['destinos'][mercadoria] = vertice
            elif tipo == 'w':       
                instancia['premios'][int(campos[1])] = float(campos[2])
            elif tipo == 'a':       
                instancia['arestas'].append((int(campos[1]), int(campos[2]), float(campos[3])))
            else:
                raise ValueError(f'{caminho}: linha  invalida: {texto.strip()}')
    return instancia

def montarPlMercadoria(instancia):
    arestas = instancia['arestas']
    qtdAresta = len(arestas)
    qtdMercadoria = instancia['qtdMercadoria']
    qtdColuna = qtdMercadoria * qtdAresta

    A = []
    b = []
    for indexAresta, (u, v, cap) in enumerate(arestas):
        coef = [0.0] * qtdColuna
        for indexMercadoria in range(qtdMercadoria):
            coef[indexMercadoria * qtdAresta + indexAresta] = 1.0
        A.append(coef)
        b.append(cap)

    for indexMercadoria in range(qtdMercadoria):
        merc = indexMercadoria + 1
        origem = instancia['origens'][merc]
        destino = instancia['destinos'][merc]
        for vertice in range(1, instancia['qtdVertice'] + 1):
            if vertice == origem or vertice == destino:
                continue
            coef = [0.0] * qtdColuna
            for indexAresta, (u, v, cap) in enumerate(arestas):
                if v == vertice:
                    coef[indexMercadoria * qtdAresta + indexAresta] += 1.0
                if u == vertice:
                    coef[indexMercadoria * qtdAresta + indexAresta] -= 1.0
            A.append(coef)
            b.append(0.0)
            A.append([-x for x in coef])
            b.append(0.0)

    c = [0.0] * qtdColuna
    for indexMercadoria in range(qtdMercadoria):
        merc = indexMercadoria + 1
        destino = instancia['destinos'][merc]
        for indexAresta, (u, v, cap) in enumerate(arestas):
            if v == destino:
                c[indexMercadoria * qtdAresta + indexAresta] = instancia['premios'][merc]

    return {'A': A, 'b': b, 'c': c}


if __name__ == '__main__':
    instancia = lerInstance('p2/mc_instance1.max')
    print('qtdVertice =', instancia['qtdVertice'],
          '| qtdMercadoria =', instancia['qtdMercadoria'])
    print('origens =', instancia['origens'], '| destinos =', instancia['destinos'],
          '| premios =', instancia['premios'])
    print('arestas =', instancia['arestas'])
    pl = montarPlMercadoria(instancia)
    for linha, bi in zip(pl['A'], pl['b']):
        print(linha, '>=', bi)
    print('c =', pl['c'])
