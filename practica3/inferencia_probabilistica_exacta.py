import re

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
clase que representa un factor
'''    
class factor:
    def __init__(self, variables, valores):
        self.valores = valores
        self.variables = variables
    
    #getters
    def get_variables(self):
        return self.variables
    
    def get_valores(self):
        return self.valores
    
    def contiene_variable(self, nombre):
        for variable in self.variables:
            if variable.get_nombre() == nombre:
                return True
        return False

    def get_variable_position(self, nombre):
        if not self.contiene_variable(nombre):
            return -1

        for i in range(len(self.variables)):
            if self.variables[i].get_nombre() == nombre:
                return i
        
        
    

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
    

        

def main():
    lector = reader("base_tablas.txt")
    lista_variables = []
    lista_factores = []

    data = lector.get_data()

    variables = data[0].split(",")
    print("--------------") 

    print(variables)

    #guardar variables
    for var in variables:
        lista_variables.append(variable(var[0],int(var[1])))

    '''
    for elem in lista_variables:
        print(elem.get_nombre())
        print(elem.get_valores())
        print(type(elem.get_valores()))
    '''    

    nodo_actual = None
    tabla_valores = None
    variables_factor = []

    def guardar_factor(tabla, variables_fact):
        if (tabla is not None) and (variables_fact):
            lista_factores.append(factor(variables_fact, tabla))

    def obtener_variable(nombre):
        for var in lista_variables:
            if var.get_nombre() == nombre:
                return var

    for datum in data[1:-2]:
        #print(datum)
        
        fila = datum.split(":")
        elementos = fila[0].split(",")
        valor = fila[1]
        
        if nodo_actual != elementos[0][0]:
            nodo_actual = elementos[0][0]
            guardar_factor(tabla_valores, variables_factor)
            
            variables_factor = []
            for elem in elementos:
                variables_factor.append(obtener_variable(elem[0]))

            print("-----")
            for var in variables_factor:
                print(var.get_nombre())

            tabla_valores = {}

            #print("-----")
            print()
            print(tabla_valores)

        llave = ""
        for elem in elementos:
            llave += elem[1]

        tabla_valores.update({llave:valor})
        
        
        eliminacion = data[-2].split(",")
        condiciones = data[-1].split(",")

        while eliminacion:
            elemento_eliminable = eliminacion.pop(0).lower()

            factores_reducibles = []
            for factor in lista_factores:
                if factor.contiene_variable(elemento_eliminable):
                    factores_reducibles.append(factor)



            while len(factores_reducibles) > 1:
                factor1 = factores_reducibles.pop()
                factor2 = factores_reducibles.pop()

                mapa_nuevo_factor = {}

                variables_comunes = factor1.get_variables()
                var_aux = factor2.get_variables()
                for var in variables_comunes:
                    if var not in var_aux:
                        variables_comunes.remove(var)

                #TODO: Saber las variables no comunes

                factor1_keys = factor1.get_valores().keys()
                factor2_keys = factor2.get_valores().keys()

                llave_maestra_1 = "^".join(["*" for i in range(len(factor1.get_variables()))]) + "$"
                llave_maestra_2 = "^".join(["*" for i in range(len(factor2.get_variables()))]) + "$"

                mapas_valores_1 = factor1.get_valores()
                mapas_valores_2 = factor2.get_valores()

                indices_factor1 = []
                indices_factor2 = []

                for var in variables_comunes:
                    indices_factor1.append(factor1.get_variable_position(var.get_nombre()))
                    indices_factor2.append(factor2.get_variable_position(var.get_nombre()))

                #TODO

                valores_actuales = [0 for i in range(len(variables_comunes))]

                # Funcion de ayuda para remover caracteres de un string
                def char_remover(string, indexes):
                    for index in sorted(indexes, reverse=True):
                        string = string[:index] + string[index+1:]
                    return string

                while True:
                    #Iterar por todas las versiones de las posibles llaves
                    for value in range(len(valores_actuales)-1,0,-1):
                        if valores_actuales[value] == variables_comunes[value].get_valores():
                            valores_actuales[value] = 0
                            valores_actuales[value-1] += 1
                    if valores_actuales[0] == factor1.get_variables()[0].get_valores():
                        break

                    #Obtener las llaves de los factores
                    llave1 = llave_maestra_1.copy()
                    llave2 = llave_maestra_2.copy()

                    #Generar las llaves de busqueda de esta iteracion
                    for i in range(len(valores_actuales)):
                        llave1[indices_factor1[i]] = valores_actuales[i]
                        llave2[indices_factor2[i]] = valores_actuales[i]

                    llaves_1 = re.search(llave1, factor1_keys)
                    llaves_2 = re.search(llave2, factor2_keys)

                    for clave in llaves_1:
                        for clave2 in llaves_2:
                            nuevo_valor = mapas_valores_1[clave] * mapas_valores_2[clave2]
                            #Generar la nueva clave y guardar el valor
                            nueva_clave = ""
                            for num in valores_actuales:
                                nueva_clave += str(num)
                            nueva_clave += char_remover(clave, indices_factor1) + char_remover(clave2, indices_factor2)
                            mapa_nuevo_factor.update({nueva_clave:nuevo_valor})

                    #Avanzar al siguiente valor
                    valores_actuales[-1] += 1

                #TODO: Generar el nuevo factor y meterlo en la lista de factores reducibles


            #TODO: Marginalizar el factor resultante


            variables_comunes = factores_reducibles[0].get_variables()

            

            
        #TODO 
        



        


    #print(data[-1])

    

if __name__ == "__main__":
    main()