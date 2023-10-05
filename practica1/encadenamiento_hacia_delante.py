
def main():
    print("Encadenamiento hacia delante")
    fichero = reader("BC_1.txt")
    print(fichero.get_data())

class regla:
    def __init__(self):
        self.clausulas = []
        self.resultado = None
        self.isHorn = None
    

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

if __name__ == "__main__":
    main()

