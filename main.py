import sys

import p1
import p2
import pulpTeste
import stoer_wagner as sw
import auxiliares as aux
import numpy as np
import primal_dual



if __name__ == '__main__':
    if(sys.argv[1] == "p1"):
        #Variaveis de entrada
        caminho = f"{sys.argv[1]}/instance{sys.argv[2]}.min"
        instancia = p1.lerInstance(caminho)
        pl = p1.montarPlCorte(instancia)
        matriz = aux.arestas_para_matriz(instancia['arestas'], instancia['qtdVertices'])
        menor_corte, melhor_particao = sw.stoer_wagner(matriz)

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

        print(f"\n===== Resultado do Algoritmo de Stoer-Wagner =====")
        print(f"Menor corte: {menor_corte:5.1f}")
        print(f"Melhor partição: {melhor_particao}")


        tableau_inicial = aux.montar_tableau(pl, 'min')
        print("\n===== Tableau Inicial Simplex =====")
        print(tableau_inicial)

        quantidadeAresta = len(instancia['arestas'])
        quantidadeVertice = instancia['qtdVertices']
        W, corteS, corteT = primal_dual.corteMinimo(tableau_inicial,quantidadeVertice, quantidadeAresta)
        print("W =", W)
        print("Lado s:", corteS)
        print("Lado t:", corteT)

        np.set_printoptions(threshold=np.inf, linewidth=250, precision=2, suppress=True)


        valor_otimo, variaveis = pulpTeste.p1_pulp(instancia)

        print(f"Valor do Corte Mínimo Pulp: {valor_otimo}")
        print("=== Variáveis Ativas (Valor > 0) ===")

        for var in variaveis:
            valor_arredondado = round(var.varValue, 5) 
            
            if valor_arredondado > 0:
                print(f"{var.name} = {valor_arredondado}")


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

        tableau_inicial = aux.montar_tableau(pl, 'max')
        quantidadeAresta =  len(instancia['arestas'])
        quantidadeMercadoria = instancia['qtdMercadoria']

        Z, fluxos = primal_dual.mercadoria(tableau_inicial, quantidadeAresta, quantidadeMercadoria)
        print("Z =", Z)
        for mercadoria, arco, valor in fluxos:
            u, v, cap = instancia['arestas'][arco]
            print(f"  Mercadoria {mercadoria}: {u:2d} -> {v:2d} : {valor}")



        valor_otimo, variaveis = pulpTeste.p2_pulp(instancia)

        print(f"Valor do Fluxo Máximo Pulp: {valor_otimo}")
        print("=== Variáveis Ativas (Valor > 0) ===")

        for var in variaveis:
            valor_arredondado = round(var.varValue, 5) 
            
            if valor_arredondado > 0:
                print(f"{var.name} = {valor_arredondado}")

