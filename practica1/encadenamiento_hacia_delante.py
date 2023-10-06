import re

base_conocimiento = {}
reglas = []
proposiciones = []

class rule:
    def __init__(self, clausulas, consecuente):
        self.clausulas = clausulas
        self.consecuente = consecuente
        self.horn = self.isHorn()
             
    def isHorn(self):
        pattern = r'^.*\+.*$'
        for clausula in self.clausulas:
            if bool(re.match(pattern, clausula)):
                return False
        return True

    def disparar(self):
        if self.consecuente in base_conocimiento:
            return False
        for clausula in self.clausulas:
            if clausula not in base_conocimiento:
                return False
        base_conocimiento.update({self.consecuente:True})
        return True

def main():
    print("Encadenamiento hacia delante")
    fichero = reader("BC_1.txt")
    # Se recorre todas las filas del fichero
    for fila in fichero.get_data():
        # Busqueda de reglas y hechos
        if (re.search("^.*:.$",fila)):
            #divido en clausulas y consecuente
            division = fila.split(":")
            clausulas, consecuente = division[0], division[1]
            clausulas = clausulas.split("*")
            reglas.append(rule(clausulas, consecuente))
        else:
            base_conocimiento.update({fila:True})

        for char in fila:
            if (re.search("[a-z]", char) and (not char in proposiciones)):
                proposiciones.append(char)
    
    loop = True
    while loop:
        loop = False
        for regla in reglas:
            loop = loop or regla.disparar()

    print(fichero.get_data())
    print(base_conocimiento.keys())
    print(proposiciones)

# *:r --> regla; lista(*) = lista proposiciones; r = conclusion
# r --> hecho
# p*q --> p and q
# p+q --> p or q (se utiliza como una unica proposicion, tiene que existir literalmente, anhade 
# incertidumbre a la completud del encadenamiento)
# () --> todo entre parentesis se comporta como una "clausula"



#def contiene(key):
    #return (hechos.get(key) not None)


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

