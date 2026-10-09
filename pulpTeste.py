import pulp

def p1_pulp(instancia):
    s = instancia['s']
    t = instancia['t']
    arestas = instancia['arestas']
    
    prob = pulp.LpProblem("Corte_Minimo", pulp.LpMinimize)
    
    x = {(u, v): pulp.LpVariable(f"x_{u}_{v}", lowBound=0) for u, v, cap in arestas}
    
    d = {vertice: pulp.LpVariable(f"d_{vertice}", lowBound=0) 
         for vertice in range(1, instancia['qtdVertices'] + 1)}
    
    prob += pulp.lpSum([cap * x[(u, v)] for u, v, cap in arestas])
    
    for u, v, cap in arestas:
        prob += x[(u, v)] >= d[v] - d[u]
        prob += x[(u, v)] >= d[u] - d[v]
        
    prob += d[s] == 0
    prob += d[t] == 1
    
    prob.solve()
    
    return pulp.value(prob.objective), prob.variables()


def p2_pulp(instancia):
    arestas = instancia['arestas']
    qtdMercadoria = instancia['qtdMercadoria']
    qtdVertice = instancia['qtdVertice']
    origens = instancia['origens']
    destinos = instancia['destinos']
    premios = instancia['premios']

    prob = pulp.LpProblem("Fluxo_Multimercadoria", pulp.LpMaximize)

    f = {}
    for i in range(1, qtdMercadoria + 1):
        for u, v, cap in arestas:
            f[(i, u, v)] = pulp.LpVariable(f"f_{i}_{u}_{v}", lowBound=0)

    objetivo = []
    for i in range(1, qtdMercadoria + 1):
        t_i = destinos[i]
        premio_i = premios[i]
        fluxo_chegando_destino = pulp.lpSum([f[(i, u, v)] for u, v, cap in arestas if v == t_i])
        objetivo.append(premio_i * fluxo_chegando_destino)
        
    prob += pulp.lpSum(objetivo)

    for u, v, cap in arestas:
        prob += pulp.lpSum([f[(i, u, v)] for i in range(1, qtdMercadoria + 1)]) <= cap

    for i in range(1, qtdMercadoria + 1):
        s_i = origens[i]
        t_i = destinos[i]
        
        for vertice in range(1, qtdVertice + 1):
            if vertice == s_i or vertice == t_i:
                continue
            
            fluxo_sai = pulp.lpSum([f[(i, u, v)] for u, v, cap in arestas if u == vertice])
            
            fluxo_entra = pulp.lpSum([f[(i, u, v)] for u, v, cap in arestas if v == vertice])
            
            prob += (fluxo_sai - fluxo_entra == 0)

    prob.solve()

    return pulp.value(prob.objective), prob.variables()