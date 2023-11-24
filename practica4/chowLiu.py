import networkx as nx
import re
import matplotlib.pyplot as plt
import math

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
    lector = reader('base_datos.txt')
    data = lector.get_data()
    longitud = len(data[1:])

    variables_text = data[0].split(',')

    print(variables_text)

    variables = []
    for var in variables_text:
        variables.append(variable(var[0],int(var[1])))

    def buscar_variable(nombre):
        for var in variables:
            if var.get_nombre() == nombre:
                return var

    diccionario = {}
    pesos = {}
    
    #contar instancias variables
    for linea in data[1:]:
        info_linea = linea.split(',')

        for i in range(1,2**len(info_linea)):
            clave = ""
            for j in range(len(info_linea)):
                if i>>j & 1:
                    clave += info_linea[j]
            print(clave)

            if clave in diccionario.keys():
                diccionario[clave] += 1
            else:
                diccionario[clave] = 1

    print(diccionario)

    #busco parejas de variables
    clave_maestra = "^.0.0$"

    llaves = diccionario.keys()
    parejas = []

    for llave in llaves:
        resultado = re.match(clave_maestra, llave)
        if resultado:
            lista_llave = list(llave)
            string = lista_llave[0].upper() + lista_llave[2].upper()
            parejas.append(string)

    print(parejas)
            

    #Calculo la informacion mutua de cada pareja de variables

    for pareja in parejas:
        elem1 = pareja[0].lower()
        elem2 = pareja[1].lower()
        valores1 = buscar_variable(elem1).get_valores()
        valores2 = buscar_variable(elem2).get_valores()

        peso = 0

        for i in range(valores1):
            for j in range(valores2):
                clave1 = elem1 + str(i)
                clave2 = elem2 + str(j)     
                peso += (diccionario[clave1+clave2] / longitud) * math.log((diccionario[clave1+clave2] / longitud) / ((diccionario[clave1] / longitud) * (diccionario[clave2] / longitud)), 2)

        pesos[pareja] = peso

    print(pesos)
if __name__ == "__main__":
    main()