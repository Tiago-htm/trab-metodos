import sys

from numpy import rint

import p1
import p2
import stoer_wagner as sw
import auxiliares as aux

if __name__ == '__main__':
    if(sys.argv[1] == "p1"):

        #Variaveis de entrada
        caminho = f"{sys.argv[1]}/instance{sys.argv[2]}.min"
        instancia = p1.lerInstance(caminho)
        pl = p1.montarPlCorte(instancia)
        matriz = aux.arestas_para_matriz(instancia['arestas'], instancia['qtdVertices'])
        resultado_sw = sw.stoer_wagner(matriz)

        valor_sw = resultado_sw['valor']
        particao_1_real = [v + 1 for v in resultado_sw['particao1']]
        particao_2_real = [v + 1 for v in resultado_sw['particao2']]

        print(f"\n[ P1 - Corte Mínimo s-t ]")
        print(f"Vértices: {instancia['qtdVertices']} | Origem (s): {instancia['s']} | Destino (t): {instancia['t']}")
        
        print("\n===== Arestas (u -> v : capacidade) =====")
        for u, v, cap in instancia['arestas']:
            print(f"  {u:2d} -> {v:2d} : {cap:5.1f}")
            
        print("\n===== Restrições (A <= b) =====")
        for linha, bi in zip(pl['A'], pl['b']):
            linha_formatada = " ".join([f"{x:4.1f}" for x in linha])
            print(f"[{linha_formatada}] <= {bi:5.1f}")

            
        print("\n===== Vetor de Custos (c) =====")
        c_formatado = " ".join([f"{x:4.1f}" for x in pl['c']])
        print(f"[{c_formatado}]")

        matriz = aux.arestas_para_matriz(instancia['arestas'], instancia['qtdVertices'])
        print("\n===== Matriz de Adjacência =====")
        print(matriz)

        print(f"\n" + "="*55)
        print(f" RESULTADO DO STOER-WAGNER (Corte Mínimo Global)")
        print("="*55)
        print(f"Custo do Corte Global : {valor_sw:5.1f}")
        print(f"Partição (A)     : {particao_1_real}")
        print(f"Resto do Grafo (B)    : {particao_2_real}")
        print("="*55)

    elif(sys.argv[1] == "p2"):
        #Variaveis de entrada
        caminho = f"{sys.argv[1]}/mc_instance{sys.argv[2]}.max"
        instancia = p2.lerInstance(caminho)
        matriz = aux.arestas_para_matriz(instancia['arestas'], instancia['qtdVertice'])
        menor_corte = sw.stoer_wagner(matriz)

        print(f"\n[ P2 - Fluxo Máximo (Múltiplas Mercadorias) ]")
        print(f"Vértices: {instancia['qtdVertice']} | Mercadorias: {instancia['qtdMercadoria']}")
        
        print("\n===== Mercadorias (Origem -> Destino : Prémio) =====")
        for m in range(1, instancia['qtdMercadoria'] + 1):
            origem = instancia['origens'][m]
            destino = instancia['destinos'][m]
            premio = instancia['premios'][m]
            print(f"  Merc {m}: {origem:2d} -> {destino:2d} | Prémio: {premio:5.1f}")

        print("\n===== Arestas (u -> v : capacidade) =====")
        for u, v, cap in instancia['arestas']:
            print(f"  {u:2d} -> {v:2d} : {cap:5.1f}")
            
        pl = p2.montarPlMercadoria(instancia)
        
        print("\n===== Restrições (A <= b) =====")
        for linha, bi in zip(pl['A'], pl['b']):
            linha_formatada = " ".join([f"{x:4.1f}" for x in linha])
            print(f"[{linha_formatada}] <= {bi:5.1f}")
            
        print("\n===== Vetor de Custos (c) =====")
        c_formatado = " ".join([f"{x:4.1f}" for x in pl['c']])
        print(f"[{c_formatado}]")

