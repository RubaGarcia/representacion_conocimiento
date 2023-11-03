

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

    for datum in data[1:-1]:
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

            tabla_valores = 0
            
            for index in range(len(variables_factor)-1, -1, -1):
                tabla_valores = [tabla_valores for num in range(variables_factor[index].get_valores())]


            #print("-----")
            print()
            print(tabla_valores)
        
        

        
    '''
    #Leer el orden de eliminacion
    lector_orden = reader("parametros.txt")
    data_orden = lector_orden.get_data()
    orden1 = data_orden[0].split(",")
    if data_orden[1] is not null:
        orden2 = data_orden[1].split(",")
        inferencia_condicional(orden1,orden2,listafactores)
    inferencia_margial(orden1, listafactores)

    def inferencia_marginal(orden1):
        for orden in orden1:


    def inferencia_condicional(orden1, orden2):

    '''




        #TODO 
        



        


    #print(data[-1])

    

if __name__ == "__main__":
    main()