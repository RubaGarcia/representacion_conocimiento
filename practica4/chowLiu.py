import networkx as nx
import re
import matplotlib.pyplot as plt
import math
import random

class reader:
    def __init__(self, file):
        self.file = file
        self.data = self.read_file()

    def read_file(self):
        with open(self.file, 'r') as f:
            data = f.readlines()
        for i in range(len(data)):
            data[i] = data[i].replace('\n', '')
        return data

    def get_data(self): 
        return self.data

'''
clase que representa las variables
'''
class variable:
    def __init__(self, nombre, valores):
        self.nombre = nombre
        self.valores = valores

    #getters
    def get_nombre(self):
        return self.nombre
    
    def get_valores(self):
        return self.valores

def print_graph(G):
    nx.draw(G, with_labels=True)
    plt.show()
 


#funcion que crea el grafo a partir de las variables(data)
def crear_grafo(data):
    G = nx.graph()
    while data:
        var = data.pop(0)
        G.add_node(var.get_nombre())
    print_graph(G)
    return G





def main():
    lector = reader('base_datos_20.txt')
    data = lector.get_data()
    longitud = len(data[1:])

    variables_text = data[0].split(',')

    print(variables_text)

    variables = []
    for var in variables_text:
        variables.append(variable(var[:-1],int(var[-1])))

    def buscar_variable(nombre):
        for var in variables:
            if var.get_nombre() == nombre:
                return var

    diccionario = {}
    pesos = {}
    
    #contar instancias variables
    for linea in data[1:]:
        info_linea = linea.split(',')

        for i in range(len(info_linea)):
            #clave = ""
            for j in range(i, len(info_linea)):
                if j == i:
                    clave = info_linea[i]
                else:
                    clave = info_linea[i] + info_linea[j]

                if clave in diccionario.keys():
                    diccionario[clave] += 1
                else:
                    diccionario[clave] = 1
                #print(clave)

    print(diccionario)

    #busco parejas de variables
    clave_maestra = "^[a-zA-z]+0[a-zA-Z]+0$"

    llaves = diccionario.keys()
    parejas = []

    for llave in llaves:
        resultado = re.match(clave_maestra, llave)
        if resultado:
            lista_llave = list(llave)
            string = ""
            for i in range(len(lista_llave)-1):
                if lista_llave[i] != '0':
                    string += lista_llave[i].upper()
                else:
                    string += "|"
            #string = lista_llave[0].upper() + "|" + lista_llave[2].upper()
            parejas.append(string)

    print(parejas)
            

    #Calculo la informacion mutua de cada pareja de variables

    for pareja in parejas:
        #elem1 = pareja[0].lower()
        #elem2 = pareja[1].lower()
        elementos = pareja.split('|')
        elem1 = elementos[0].lower()
        elem2 = elementos[1].lower()
        valores1 = buscar_variable(elem1).get_valores()
        valores2 = buscar_variable(elem2).get_valores()

        peso = 0

        for i in range(valores1):
            for j in range(valores2):
                clave1 = elem1 + str(i)
                clave2 = elem2 + str(j)     
                
                peso += (diccionario[clave1+clave2] / longitud) * math.log((diccionario[clave1+clave2] / longitud) / ((diccionario[clave1] / longitud) * (diccionario[clave2] / longitud)), 2)

        
        pesos.update({(elem1+"|"+elem2): peso})

    #ordenamos los pesos de mayor a menor

    pesos_ordenados = sorted(pesos.items(), reverse=False)
    print("--------------------")
    print (pesos_ordenados)
    print("--------------------")
        

    #Construimos el arbol de recubrimiento con los pesos maximos
    #aristas_escogidas = pesos_ordenados[:len(variables)-1]
    #print(aristas_escogidas)

    #Grafo de recubrimiento
    G = nx.Graph()
    for var in variables:
        G.add_node(var.get_nombre())
    #print_graph(G)
    '''
    for arista in aristas_escogidas:
        nodos = arista[0].split('|')
        G.add_edge(nodos[0], nodos[1])
    print_graph(G)
    '''

    #Creamos el arbol de pesos minimos
    nodos_visitados = []
    while(len(G.edges) != len(variables)-1):
        arista = pesos_ordenados.pop(0)
        aristas = arista[0].split('|')
        if (aristas[0] in nodos_visitados) and (aristas[1] in nodos_visitados):
            continue

        G.add_edge(aristas[0], aristas[1], weight=arista[1])
        if aristas[0] not in nodos_visitados:
            nodos_visitados.append(aristas[0])
        if aristas[1] not in nodos_visitados:
            nodos_visitados.append(aristas[1])
    print_graph(G)

    dirG = nx.DiGraph()
    dirG.add_nodes_from(G.nodes)

    nodos_direccionalidad = [random.choice(variables).get_nombre()]
    nodos_visitados = []

    while(nodos_direccionalidad):
        nodo = nodos_direccionalidad.pop(0)
        nodos_visitados.append(nodo)
        for vecino in G.edges(nodo):
            otro_nodo = vecino[1]
            if otro_nodo not in nodos_visitados:
                nodos_direccionalidad.append(otro_nodo)
                dirG.add_edge(nodo, otro_nodo)

    print_graph(dirG)
    

    
        
if __name__ == "__main__":
    main()