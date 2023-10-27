import random


j = 0
while j < 10:
    # Program to show various ways to read and
    # write data in a file.
    string = "grafo"+str(j+4)+".txt"
    file1 = open(string,"w")
    
    # \n is placed to indicate EOL (End of Line)
    numero_nodos = random.randint(3,70)
    file1.write(str(numero_nodos) + "\n")
    numero_aristas = random.randint(numero_nodos, 2*numero_nodos)
    for i in range(numero_aristas):
        nodo1 = random.randint(0,numero_nodos-1)
        nodo2 = random.randint(0,numero_nodos-1)
        while nodo1 == nodo2:
            nodo2 = random.randint(0,numero_nodos-1)
        
        file1.write(str(nodo1) + "," + str(nodo2) + "\n")

    nodo1_independencia = random.randint(0,numero_nodos-1)
    nodo2_independencia = random.randint(0,numero_nodos-1)
    while nodo1_independencia == nodo2_independencia:
        nodo2_independencia = random.randint(0,numero_nodos-1)

    observados = []
    for i in range(random.randint(0,numero_nodos-1)):
        observados.append(random.randint(0,numero_nodos-1))

    for elem in observados:
        if elem == nodo1_independencia or elem == nodo2_independencia:
            observados.remove(elem)

    file1.write(str(nodo1_independencia) + "," + str(nodo2_independencia) + "," + str(observados))
    file1.close() #to change file access modes
    j+=1