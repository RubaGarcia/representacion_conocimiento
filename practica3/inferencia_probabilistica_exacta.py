

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
    
class factor:
    def __init__(self, variables, valores):
        self.valores = valores
        self.variables = variables
        
        

class variable:
    def __init__(self, nombre, valores):
        self.nombre = nombre
        self.valores = valores
    
def main():
    lector = reader("base_tablas.txt")
    lista_variables = []

    for datum in lector.get_data()[:-1]:
        print(datum)
        fila = datum.split(":")
        elementos = fila[0].split(",")
        valor = fila[1]
        variables = []

        #TODO


    print(lector.get_data()[-1])

    

if __name__ == "__main__":
    main()