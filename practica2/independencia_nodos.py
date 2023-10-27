import networkx as nx
import matplotlib.pyplot as plt

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

def main():
    grafo = nx.DiGraph()

    data = reader("grafo10.txt").get_data()

    #numero de nodos
    nNodos = int(data[0])
    
    #creo los nodos en el grafico
    for num in range(nNodos):
        grafo.add_node(num)

    #creo las aristas de los nodos
    for fila in range(1, len(data) - 1):
        nodos = data[fila].split(",")
        grafo.add_edge(int(nodos[0]), int(nodos[1]))

    #print_graph(grafo)    

    #independencia a comprobar
    independencia = data[-1].split(",")
    nodo1 = int(independencia[0])
    nodo2 = int(independencia[1])
    observados = independencia[2][1:-1]
    lista_observados = []
    for elem in observados.split("."):
        lista_observados.append(int(elem))

    lista_no_eliminables = lista_observados.copy()
    lista_no_eliminables.append(nodo1)
    lista_no_eliminables.append(nodo2)
    
    #print_graph(grafo)

    eliminacion_hojas(grafo,lista_no_eliminables)

    print_graph(grafo)

    nuevo_grafo = union_padres(grafo)

    print_graph(nuevo_grafo)

    #se elimina los nodos observados
    nuevo_grafo.remove_nodes_from(lista_observados)

    #busqueda en grafos para conprobar su independencia
    dependencia = explorar(nuevo_grafo, nodo1, nodo2)

    if dependencia:
        print("El nodo " + str(nodo1) + " y el nodo " + str(nodo2) + " no son independientes")
    else:
        print("El nodo " + str(nodo1) + " y el nodo " + str(nodo2) + " son independientes")
  
    

def eliminacion_hojas(grafo, lista_no_eliminables):
    print("Eliminacion de los vertices hoja")

    #1. Eliminacion de los vertices hoja
    nodosHoja = []

    for nodo in grafo:
        #grafo.edges te devuelve el nodo actual y el hijo
        if len(grafo.edges(nodo)) == 0:
            nodosHoja.append(nodo)

    while(nodosHoja):
        nodo = nodosHoja.pop()
        if (nodo not in lista_no_eliminables):
            padres = grafo.predecessors(nodo)
            for padre in padres:
                if padre not in nodosHoja:
                    nodosHoja.append(padre)
            grafo.remove_node(nodo)

def union_padres(grafo):
    
    #Se une todos los padres con hijos comunes
    for nodo in grafo:
        padres = list(grafo.predecessors(nodo))
        uniones = []
        for i in range(len(padres)):
            for j in range(len(padres[i:])):
                if i != j:
                    uniones.append((padres[i],padres[j]))
        grafo.add_edges_from(uniones)

    #Convertir los grafos en no dirigidos
    non_dir_grafo = nx.Graph()
    non_dir_grafo.add_nodes_from(list(grafo))
    non_dir_grafo.add_edges_from(grafo.edges)
    
    return non_dir_grafo

def explorar(grafo, nodo_inicial, nodo_final):
    #se explora en profundidad (pila)
    busqueda = [nodo_inicial]
    explorados = []

    while busqueda:
        nodo_exploracion = busqueda.pop(0)
        explorados.append(nodo_exploracion)

        nodos_vecinos = grafo.neighbors(nodo_exploracion)

        if (nodo_final in nodos_vecinos):
            return True
        
        for nodo in nodos_vecinos:
            if nodo not in explorados:
                busqueda.append(nodo)

    return False
    
def print_graph(G):
    nx.draw(G)
    plt.show()
    plt.pause(2)
    plt.close()
    

if __name__ == "__main__":
    main()
