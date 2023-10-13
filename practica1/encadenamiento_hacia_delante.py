import re


'''
1: caso
-reglas CH (completo)
-hechos CH (completo)
BASES: BC_3.txt
2: caso (puede ser incompleto)
-reglas noCH
-hecho CH
BASES: BC_1.txt (es incompleta), BC_2.txt (es incompleta)
3: caso (puede ser incompleto)
-reglas noCH
-hecho noCH
BASES: BC_4.txt (es completa)
'''


base_conocimiento = {}
reglas = []
proposiciones = []
hechos = []

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
    fichero = reader("BC_3.txt")
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

    print(fichero.get_data())
    base_completa = []
    for elem in base_conocimiento.keys():
        base_completa.append(elem)
    print(base_completa)
    print(proposiciones)

    valores_proposiciones_bool = [[] for i in range(len(proposiciones))]
    for i in range(2 ** len(proposiciones)):
        for j in range(len(proposiciones)):
            valores_proposiciones_bool[j].append(bool(i & (2 ** j)))
    
    def obtener_valor(elem):
        if re.search("^.{1}$", elem):
            return valores_proposiciones_bool[proposiciones.index(elem)]
        else:
            lista_or = elem.split("+")
            valor = False
            lista_valores = []
            for elem in lista_or:
                lista_valores.append(obtener_valor(elem))

            lista_retorno = lista_valores[0]
            
            for i in range(len(lista_retorno)):
                for lista in lista_valores[1:]:
                    lista_retorno[i] = lista_retorno[i] or lista[i]
            return lista_retorno

    valores_tablas_elementos = []
    for elem in hechos:
        valores_tablas_elementos.append(obtener_valor(elem))

    for regla in reglas:
        lista_valores_clausulas = []
        valores_consecuente = obtener_valor(regla.consecuente)
        for clausula in regla.clausulas:
            lista_valores_clausulas.append(obtener_valor(clausula))

        for i in range(len(valores_consecuente)):
            valor_clausulas = True
            for lista in lista_valores_clausulas:
                valor_clausulas = valor_clausulas and lista[i]

            #TODO: PROBLEMA AQUI
            valores_consecuente[i] = (not valor_clausulas) or valores_consecuente[i]

        valores_tablas_elementos.append(valores_consecuente)

        

    '''
    # Comprobacion de completitud
    valores_proposiciones_bool = [[] for i in range(len(proposiciones))]
    lista_reglas = []
    lista_consecuentes = []
    for regla in reglas:
        lista_reglas.append(regla.clausulas)
        lista_consecuentes.append(regla.consecuente)

    BC_tabla_verdad_bool = []

    # Inicio de la comprobacion por tabla de verdad
    for i in range(2 ** len(proposiciones)):
        for j in range(len(proposiciones)):
            valores_proposiciones_bool[j].append(bool(i & (2 ** j)))
        
        valor_tabla = True

        for regla in lista_reglas:
            valor_regla = True
            indice_regla = lista_reglas.index(regla)
            
            for condicion in regla:
                valor_condicion = True

                if (re.search("^.{1}$", condicion)):
                    # Si el elemento es solo una letra, tomar su valor
                    indice = proposiciones.index(condicion)
                    valor_condicion = valores_proposiciones_bool[indice][i]
                else:
                    # Si el elemento no es solo una letra, es un or entre distintas proposiciones
                    lista_or = condicion.split("+")
                    
                    # Dividir la lista de or en sus elementos y e ir acumulando su valor
                    valor_condicion = False
                    for elem in lista_or:
                        indice = proposiciones.index(elem)
                        valor_condicion = valor_condicion or valores_proposiciones_bool[indice][i]

                #print(str(valor_condicion) + " " + str(condicion))
                
                #print(str(valor_condicion) + " " + proposiciones[indice_consecuente] + " " 
                      #+ str(valores_proposiciones_bool[indice_consecuente][i]) + " " + str(i))


                #El valor de la regla es el and entre todas sus condiciones
                valor_regla = valor_regla and valor_condicion

            indice_consecuente = proposiciones.index(lista_consecuentes[indice_regla])
            valor_regla = (not valor_regla) or valores_proposiciones_bool[indice_consecuente][i]
            # El valor de la tabla es el and entre todas las reglas
            valor_tabla = valor_tabla and valor_regla

        # Se añade el valor de la tabla a la lista de valores de la base de conocimiento
        BC_tabla_verdad_bool.append(valor_tabla)
    
    # Se asumen que todas las proposiciones estan en la base de conocimiento
    BC_tabla_verdad = proposiciones.copy()

    # Comprobar cuales de las proposiciones estan en la base de conocimiento
    for i in range(len(valores_proposiciones_bool)):
        for j in range(len(BC_tabla_verdad_bool)):
            # Si en la tabla de verdad es cierto un valor y en la proposicion es falso,
            # se elimina de la base de conocimiento
            if (not valores_proposiciones_bool[i][j] and BC_tabla_verdad_bool[j]):
                BC_tabla_verdad.remove(proposiciones[i])
                break

    print(BC_tabla_verdad_bool)
    #print(valores_proposiciones_bool)
    print(BC_tabla_verdad)
    

    # Asumimos de primeras que la base de conocimiento es completa
    completa = True
    # Comprobar que todos los elementos de la tabla de verdad estan en la base de conocimiento que hemos obtenido
    # por el encadenamiento hacia delante
    for elem in BC_tabla_verdad:
        if not elem in base_completa:
            completa = False
            break
        
    if completa:
        print("La base de conocimiento es completa")
    else:
        print("La base de conocimiento no es completa")
        '''

    
    

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

