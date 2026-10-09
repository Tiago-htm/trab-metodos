
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
def corteMinimo(tableau):
    quantidadeR = tableau.shape[0] -1
    quantidadeColuna = tableau.shape[1]
    #
    inicioFolga =  quantidadeColuna - quantidadeR -1
    #a base é quantidade de restrições que existem!!
    base = list(range(inicioFolga, inicioFolga+quantidadeR))
    print("aaaaaaaaaaaaaaaaaa")
    print(base)
