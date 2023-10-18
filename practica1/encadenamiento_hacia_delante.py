import re


'''
1: caso
-reglas CH (completo)
-hechos CH (completo)
BASES: BC_3.txt
2: caso (puede ser incompleto)
-reglas noCH
-hecho CH
BASES: BC_1.txt (es incompleta), BC_2.txt (es incompleta), BC_5.txt (es completa)
3: caso (puede ser incompleto)
-reglas noCH
-hecho noCH
BASES: BC_4.txt (es completa), BC_6.txt (es incompleta)
'''


base_conocimiento = {}
reglas = []
proposiciones = []
hechos = []

class rule:
    def __init__(self, clausulas, consecuente):
        self.clausulas = clausulas
        self.consecuente = consecuente

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
    fichero = reader("BC_6.txt")
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
            hechos.append(fila)

        for char in fila:
            if (re.search("[a-z]", char) and (not char in proposiciones)):
                proposiciones.append(char)
    
    loop = True
    while loop:
        loop = False
        for regla in reglas:
            loop = loop or regla.disparar()

    base_completa = []
    for elem in base_conocimiento.keys():
        base_completa.append(elem)

    print("BC encadenamiento hacia delante:\t", base_completa)

    valores_proposiciones_bool = [[] for i in range(len(proposiciones))]
    for i in range(2 ** len(proposiciones)):
        for j in range(len(proposiciones)):
            valores_proposiciones_bool[j].append(bool(i & (2 ** j)))
    
    def obtener_valor(elem):
        if re.search("^.{1}$", elem):
            return valores_proposiciones_bool[proposiciones.index(elem)].copy()
        else:
            lista_or = elem.split("+")
            lista_valores = []
            for elem in lista_or:
                lista_valores.append(obtener_valor(elem))

            lista_retorno = lista_valores[0]
            
            for i in range(len(lista_retorno)):
                for lista in lista_valores[1:]:
                    lista_retorno[i] = lista_retorno[i] or lista[i]
            return lista_retorno

    #Lista que contendra los valores booleanos de todos los elementos de la base de conocimiento
    valores_tablas_elementos = []
    #Obtener los valores de verdad de los hechos y añadirlos a la lista
    for elem in hechos:
        valores_tablas_elementos.append(obtener_valor(elem))

    #Obtener los valores de verdad de las reglas y añadirlos a la lista
    for regla in reglas:
        #Lista que contendra los valores booleanos de todas las clausulas de la regla (parte izquierda)
        lista_valores_clausulas = []
        #Valores booleanos del consecuente (parte derecha)
        valores_consecuente = obtener_valor(regla.consecuente)
        #Obtener los valores booleanos de las clausulas y añadirlos a la lista
        for clausula in regla.clausulas:
            lista_valores_clausulas.append(obtener_valor(clausula))

        #Obtener la tabla de verdad de la regla
        for i in range(len(valores_consecuente)):
            valor_clausulas = True
            for lista in lista_valores_clausulas:
                valor_clausulas = valor_clausulas and lista[i]

            valores_consecuente[i] = (not valor_clausulas) or valores_consecuente[i]

        valores_tablas_elementos.append(valores_consecuente)

    BC_tabla_verdad_bool = []
    #Obtener la tabla de verdad de la base de conocimiento
    for i in range(len(valores_proposiciones_bool[0])):
        valor_tabla = True
        for elem in valores_tablas_elementos:
            valor_tabla = valor_tabla and elem[i]
        BC_tabla_verdad_bool.append(valor_tabla)

    BC_tabla_verdad = proposiciones.copy()

    # Comprobar cuales de las proposiciones estan en la base de conocimiento
    for i in range(len(valores_proposiciones_bool)):
        for j in range(len(BC_tabla_verdad_bool)):
            # Si en la tabla de verdad es cierto un valor y en la proposicion es falso,
            # se elimina de la base de conocimiento
            if (not valores_proposiciones_bool[i][j] and BC_tabla_verdad_bool[j]):
                BC_tabla_verdad.remove(proposiciones[i])
                break

    print("BC tabla de verdad:\t\t\t", BC_tabla_verdad)

    # Comprobar que todos los elementos de la tabla de verdad estan en
    # la base de conocimiento que hemos obtenido por el encadenamiento hacia delante
    completa = True
    for elem in BC_tabla_verdad:
        if not elem in base_completa:
            completa = False
            break

    if completa:
        print("La base de conocimiento es completa")
    else:
        print("La base de conocimiento no es completa")





# *:r --> regla; lista(*) = lista proposiciones; r = conclusion
# r --> hecho
# p*q --> p and q
# p+q --> p or q (se utiliza como una unica proposicion, tiene que existir literalmente, anhade 
# incertidumbre a la completud del encadenamiento)

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

