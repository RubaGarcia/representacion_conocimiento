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
class facto:
    def __init__(self, variables, valores):
        self.valores = valores
        self.variables = variables
    
    #getters
    def get_variables(self):
        return self.variables
    
    def get_valores(self):
        return self.valores
    
    def contiene_variable(self, nombre):
        for i in range(len(self.variables)):
            if self.variables[i].get_nombre() == nombre:
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
            lista_factores.append(facto(variables_fact, tabla))

    def obtener_variable(nombre):
        for var in lista_variables:
            if var.get_nombre() == nombre:
                return var
            
    # Funcion de ayuda para remover caracteres de un string
    def char_remover(string, indexes):
        for index in sorted(indexes, reverse=True):
            string = string[:index] + string[index+1:]
        return string

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

        tabla_valores.update({llave:float(valor)})
        
    guardar_factor(tabla_valores, variables_factor)

    print("-----")
    print(tabla_valores)
    '''
    print("-----")
    print("lista factores")
    print(lista_factores)

    print("=====")
    for factor in lista_factores:
        vars = factor.get_variables()
        print(vars)
        print(factor.get_valores())
        print("///////////")
        for var in vars:
            print(var.get_nombre())
            print(var.get_valores())

    print("----------")
    print(lista_variables)
    print("=====")
    for var in lista_variables:
        print(var.get_nombre())
        print(var.get_valores())
    '''

    eliminacion = data[-2].split(",")
    condiciones = data[-1].split(",")


    while eliminacion:
        #Obtener la variable que se quiere eliminar
        elemento_eliminable = eliminacion.pop(0).lower()

        print("-----")
        print(elemento_eliminable)
        print(lista_factores)

        #Obtener los factores que contienen la variable
        factores_reducibles = []
        for factor in lista_factores:
            if factor.contiene_variable(elemento_eliminable):
                print("la contiene")
                factores_reducibles.append(factor)

        for factor in factores_reducibles:
            lista_factores.remove(factor)

        for factor in lista_factores:
            if factor.contiene_variable(elemento_eliminable):
                print("faltan_elementos")

        if len(factores_reducibles) == 1:
            continue

        #Mientras esa lista contenga mas de un factor, combinarlos
        while len(factores_reducibles) > 1:
            print(len(factores_reducibles))
            # Obtener los dos ultimos factores
            factor1 = factores_reducibles.pop()
            factor2 = factores_reducibles.pop()

            mapa_nuevo_factor = {}

            print("===========")
            print(factor1.get_variables())
            print(factor1.get_valores())
            print(factor2.get_variables())
            print(factor2.get_valores())

            # Encontrar sus variables comunes
            variables_comunes = []
            var_aux_1 = factor1.get_variables().copy()
            var_aux_2 = factor2.get_variables().copy()
            for var in var_aux_1:
                for var2 in var_aux_2:
                    if var.get_nombre() == var2.get_nombre():
                        variables_comunes.append(var)
                        break

            # Encontrar las variables no comunes
            variables_no_comunes = []
            for var in var_aux_1:
                if var not in variables_comunes:
                    variables_no_comunes.append(var)
            for var in var_aux_2:
                if var not in variables_comunes:
                    variables_no_comunes.append(var)

            print("/=/=/=")
            print(variables_comunes)
            print(variables_no_comunes)

            # Generar la lista de variables del nuevo factor
            # TODO: IMPORTANTE, NO ESTA BIEN PUESTO EL ORDEN DE LAS VARIABLES
            # HAY QUE ARREGLARLO
            nuevo_factor_lista_variables = variables_comunes.copy()
            for var in variables_no_comunes:
                nuevo_factor_lista_variables.append(var)
            factor1_keys = factor1.get_valores().keys()
            factor2_keys = factor2.get_valores().keys()

            # Generar las llaves maestras de los factores
            #llave_maestra_1 = "^".join(["." for i in range(len(factor1.get_variables()))]) + "$"
            #llave_maestra_2 = "^".join(["." for i in range(len(factor2.get_variables()))]) + "$"
            print("generar llaves maestras")

            # Obtener los mapas de valores de los factores
            mapas_valores_1 = factor1.get_valores()
            mapas_valores_2 = factor2.get_valores()

            # Obtener los indices de las variables comunes, para poder iterar sobre ellas
            indices_factor1 = []
            indices_factor2 = []
            for var in variables_comunes:
                indices_factor1.append(factor1.get_variable_position(var.get_nombre()))
                indices_factor2.append(factor2.get_variable_position(var.get_nombre()))

            # Mantener los indices de las variables comunes para poder buscar las llaves
            valores_actuales = [0 for i in range(len(variables_comunes))]

                

            while True:
                #Iterar por todas las versiones de las posibles llaves
                for value in range(len(valores_actuales)-1,0,-1):
                    if valores_actuales[value] == variables_comunes[value].get_valores():
                        valores_actuales[value] = 0
                        valores_actuales[value-1] += 1
                if valores_actuales[0] == factor1.get_variables()[0].get_valores():
                    break

                #Obtener las llaves de los factores
                llave1 = ["." for i in range(len(factor1.get_variables()))]
                llave2 = ["." for i in range(len(factor2.get_variables()))]

                #Generar las llaves de busqueda de esta iteracion
                for i in range(len(valores_actuales)):
                    llave1[indices_factor1[i]] = str(valores_actuales[i])
                    llave2[indices_factor2[i]] = str(valores_actuales[i])

                llave_busqueda_1 = "^"
                for elem in llave1:
                    llave_busqueda_1 += elem
                llave_busqueda_1 += "$"
                llave_busqueda_2 = "^"
                for elem in llave2:
                    llave_busqueda_2 += elem
                llave_busqueda_2 += "$"

                print(llave_busqueda_1)
                print(llave_busqueda_2)

                llaves_1 = []
                for llave in factor1_keys:
                    value = re.search(llave_busqueda_1, llave)
                    if value:
                        llaves_1.append(value.string)

                llaves_2 = []
                for llave in factor2_keys:
                    value = re.search(llave_busqueda_2, llave)
                    if value:
                        llaves_2.append(value.string)


                print(llaves_1)
                print(llaves_2)

                for clave in llaves_1:
                    for clave2 in llaves_2:
                        nuevo_valor = mapas_valores_1[clave] * mapas_valores_2[clave2]
                        #Generar la nueva clave y guardar el valor
                        nueva_clave = ""
                        for num in valores_actuales:
                            nueva_clave += str(num)
                        nueva_clave = nueva_clave + char_remover(clave, indices_factor1) + char_remover(clave2, indices_factor2)
                        mapa_nuevo_factor.update({nueva_clave:nuevo_valor})

                #Avanzar al siguiente valor
                valores_actuales[-1] += 1

            #Actualizar la lista con el nuevo factor
            factores_reducibles.append(facto(nuevo_factor_lista_variables, mapa_nuevo_factor))
            print("-----")
            print("bye")
            print(nuevo_factor_lista_variables)
            print(mapa_nuevo_factor)

        factor_marginalizar = factores_reducibles[0]
        indice_marginalizar = factor_marginalizar.get_variable_position(elemento_eliminable)
        variables_marginalizar = factor_marginalizar.get_variables().copy()
        #Eliminar la variable a marginalizar
        variables_marginalizar.pop(indice_marginalizar)
        print("/////")
        print(variables_marginalizar)

        llave_maestra_marginalizar = "^".join(["." for i in range(len(factor_marginalizar.get_variables()))]) + "$"
        valores_actuales_marginalizar = [0 for i in range(len(factor_marginalizar.get_variables()))]
        mapa_marginalizado = {}

        print(factor_marginalizar)

        # Marginalizar la variable del factor
        while True:
            #Iterar por todas las versiones de las posibles llaves
            for value in range(len(valores_actuales_marginalizar)-1,0,-1):
                if valores_actuales_marginalizar[value] == factor_marginalizar.get_variables()[value].get_valores() or value == indice_marginalizar:
                    valores_actuales_marginalizar[value] = 0
                    valores_actuales_marginalizar[value-1] += 1
            if indice_marginalizar == 0 and valores_actuales_marginalizar[0] != 0:
                break
            elif valores_actuales_marginalizar[0] == factor_marginalizar.get_variables()[0].get_valores():
                break

            #Obtener las llaves de los factores
            lista_llave = ["." for i in range(len(factor_marginalizar.get_variables()))]
            for i in range(len(valores_actuales_marginalizar)):
                lista_llave[i] = str(valores_actuales_marginalizar[i])
            lista_llave[indice_marginalizar] = "."
            llave_trabajo = "^"
            for elem in lista_llave:
                llave_trabajo += elem
            llave_trabajo += "$"	

            print(len(factor_marginalizar.get_variables()))
            print(llave_trabajo)
            

            llaves = []
            for llave in factor_marginalizar.get_valores().keys():
                value = re.search(llave_trabajo, llave)
                if value:
                    llaves.append(value.string)
            valor_actualizado = 0
            for clave in llaves:
                valor_actualizado += factor_marginalizar.get_valores()[clave]
            nueva_clave = ""
            for i in range(len(lista_llave)):
                if i != indice_marginalizar:
                    nueva_clave += lista_llave[i]

            mapa_marginalizado.update({nueva_clave:valor_actualizado})
            valores_actuales_marginalizar[-1] += 1

            
        # Actualizar la lista con el nuevo factor marginalizado
        print(mapa_marginalizado)
        print(variables_marginalizar)
        guardar_factor(mapa_marginalizado, variables_marginalizar)

            

            
    print("=======")
    print(lista_factores)
    for factor in lista_factores:
        print(factor.get_variables())
        print(factor.get_valores())
        print("///////////")
        for var in factor.get_variables():
            print(var.get_nombre())
            print(var.get_valores())
        



        


    #print(data[-1])

    

if __name__ == "__main__":
    main()