import re
import sys

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
    

        

def main(base):
    lectura = "base_tablas_"+ str(base) + ".txt"
    print (lectura)
    lector = reader(lectura)
    #lector = reader("base_tablas_0.txt")
    lista_variables = []
    lista_factores = []
    lista_constantes = []

    data = lector.get_data()

    variables = data[0].split(",")

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

    '''
    Funcion que permite guardar un factor en la lista de factores
    '''
    def guardar_factor(tabla, variables_fact):
        if (tabla is not None) and (variables_fact):
            lista_factores.append(facto(variables_fact, tabla))

    '''
    Funcion que permite obtener una variable de la lista de variables
    '''
    def obtener_variable(nombre):
        for var in lista_variables:
            if var.get_nombre() == nombre:
                return var
            
    '''
    Funcion de ayuda para remover caracteres de un string
    '''
    def char_remover(string, indexes):
        for index in sorted(indexes, reverse=True):
            string = string[:index] + string[index+1:]
        return string

    # Guardar los factores
    for datum in data[1:-2]:
        fila = datum.split(":")
        elementos = fila[0].split(",")
        valor = fila[1]
        
        # Si el nodo actual es diferente al nodo de la fila, guardar el factor (hemos cambiado de factor)
        if nodo_actual != elementos[0][0]:
            nodo_actual = elementos[0][0]
            guardar_factor(tabla_valores, variables_factor)
            
            # Inicializar la lista de variables del nuevo factor
            variables_factor = []
            for elem in elementos:
                variables_factor.append(obtener_variable(elem[0]))

            # Inicializar el mapa de valores del nuevo factor
            tabla_valores = {}

        # Generar la llave del nuevo valor
        llave = ""
        for elem in elementos:
            llave += elem[1]
        tabla_valores.update({llave:float(valor)})
        
    guardar_factor(tabla_valores, variables_factor)

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

    # Obtener la lista de variables a eliminar y cuales son condicionales
    eliminacion = data[-2].split(",")
    condiciones = data[-1].split(",")

    # Si hay condiciones, modificar los factores que contengan las variables condicionadas
    if condiciones[0] != "None":
        factores_condicionados = []
        # Comprobar por cada variable condicionada
        for var_condicionada in condiciones:
            # Obtener los factores que estan condicionados por la variable
            for factor in lista_factores:
                if factor.contiene_variable(var_condicionada[0].lower()):
                    factores_condicionados.append(factor)
            
            for factor in factores_condicionados:
                lista_factores.remove(factor)

            # Eliminar el resto de intancias de la variable
            for factor in factores_condicionados:
                indice_var = factor.get_variable_position(var_condicionada[0].lower())
                llave_cond = ["." for i in range(len(factor.get_variables()))]
                llave_cond[indice_var] = var_condicionada[1]
                llave_busqueda_cond = "^"
                for elem in llave_cond:
                    llave_busqueda_cond += elem
                llave_busqueda_cond += "$"

                # Quedarse solo con las que cumplan la condicion
                llaves_cond = []
                for llave in factor.get_valores().keys():
                    value = re.search(llave_busqueda_cond, llave)
                    if value:
                        llaves_cond.append(value.string)

                # Construir el nuevo factor ya condicionado
                viejo_mapa = factor.get_valores()
                nuevo_mapa = {}

                nuevas_variables = factor.get_variables().copy()
                nuevas_variables.pop(indice_var)

                if len(nuevas_variables) == 0:
                    # Si ya no es afectado por variables, es una constante
                    lista_constantes.append(viejo_mapa[llaves_cond[0]])
                else:
                    for clave in llaves_cond:
                        valor = viejo_mapa[clave]
                        nueva_clave = char_remover(clave, [indice_var])
                        nuevo_mapa.update({nueva_clave:valor})
                    guardar_factor(nuevo_mapa, nuevas_variables)


    while eliminacion:
        #Obtener la variable que se quiere eliminar
        elemento_eliminable = eliminacion.pop(0).lower()


        #Obtener los factores que contienen la variable
        factores_reducibles = []
        for factor in lista_factores:
            if factor.contiene_variable(elemento_eliminable):
                factores_reducibles.append(factor)

        for factor in factores_reducibles:
            lista_factores.remove(factor)

        #Si no hay factores que contengan la variable, continuar
        if len(factores_reducibles) == 0:
            continue

        #Mientras esa lista contenga mas de un factor, combinarlos
        while len(factores_reducibles) > 1:
            # Obtener los dos ultimos factores
            factor1 = factores_reducibles.pop()
            factor2 = factores_reducibles.pop()

            mapa_nuevo_factor = {}

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

            # Generar la lista de variables del nuevo factor
            nuevo_factor_lista_variables = variables_comunes.copy()
            for var in variables_no_comunes:
                nuevo_factor_lista_variables.append(var)
            factor1_keys = factor1.get_valores().keys()
            factor2_keys = factor2.get_valores().keys()

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

                # Construir las llaves de busqueda
                llave_busqueda_1 = "^"
                for elem in llave1:
                    llave_busqueda_1 += elem
                llave_busqueda_1 += "$"
                llave_busqueda_2 = "^"
                for elem in llave2:
                    llave_busqueda_2 += elem
                llave_busqueda_2 += "$"

                # Quedarse solo con las que cumplan la condicion
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

                # Combinar los valores de los factores
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

        #Obtener el factor a marginalizar (solo deberia quedar 1)
        factor_marginalizar = factores_reducibles[0]
        indice_marginalizar = factor_marginalizar.get_variable_position(elemento_eliminable)
        variables_marginalizar = factor_marginalizar.get_variables().copy()
        #Eliminar la variable a marginalizar
        variables_marginalizar.pop(indice_marginalizar)

        #Si no hay variables a marginalizar, continuar (queda como 1, no afecta en los productos)
        if len(variables_marginalizar) == 0:
            continue

        # Generar la llave maestra de marginalizacion
        llave_maestra_marginalizar = "^".join(["." for i in range(len(factor_marginalizar.get_variables()))]) + "$"
        valores_actuales_marginalizar = [0 for i in range(len(factor_marginalizar.get_variables()))]
        mapa_marginalizado = {}

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
            
            # Marginalizacion de la variable
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
        guardar_factor(mapa_marginalizado, variables_marginalizar)        


    # Escribir de manera elegante la respuesta
    texto = ""

    for factor in lista_factores[:-1]:
        texto += "("
        for var in factor.get_variables()[:-1]:
            texto += var.get_nombre() + ","
        texto += factor.get_variables()[-1].get_nombre() + ")"
        texto += " * "
    
    texto += "("
    for var in lista_factores[-1].get_variables()[:-1]:
        texto += var.get_nombre() + ","
    texto += lista_factores[-1].get_variables()[-1].get_nombre() + ")"

    for constante in lista_constantes:
        texto += " * " + str(constante)

    print(texto)

    

if __name__ == "__main__":
    
    if len(sys.argv) >= 2:
        print(sys.argv[1])
        main(sys.argv[1])
    else:
        print("no hay entrada")

    