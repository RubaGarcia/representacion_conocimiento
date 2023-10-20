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

    data = reader("grafo1.txt").get_data()

    #numero de nodos
    nNodos = data[0]

    #creo los nodos en el grafico
    for num in range(nNodos):
        grafo.add_node(num)

    #creo las aristas de los nodos
    for fila in range(1, len(data) - 1):
        nodos = fila.split(",")
        grafo.add_edge(nodos[0], nodos[1])

    

    #independencia a comprobar
    independencia = data[-1].split(",")
    inde1 = independencia[0]
    inde2 = independencia[1]
    listaobsevados = independencia[2]





def print_graph(G):
    nx.draw(G)
    plt.show()
    

if __name__ == "__main__":
    main()
