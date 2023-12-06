import sys
import random

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 
            'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 
            's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# Constante que indica cuantos valores distintos puede tomar cada variable
# (en este caso, solo 0 y 1)
VALORES_VARIABLES = 2

def main(num_variables):
    variables = []
    valores = [0 for i in range (int(num_variables))]

    for i in range(int(num_variables)):
        numero = i
        string = alphabet[numero%26]
        while numero >= 26:
            numero = numero//26 - 1
            string = alphabet[numero%26] + string

        variables.append(string)

    random.shuffle(variables)

    archivo = open("base_datos_" + str(num_variables) + ".txt", "w")
    primera_linea = variables[0] + str(VALORES_VARIABLES)
    for elem in variables[1:]:
        primera_linea += "," + elem + str(VALORES_VARIABLES)

    archivo.write(primera_linea)
    #archivo.close()

    def avanzar():
        valores[-1] += 1
        for i in range(len(valores)-1, 0, -1):
            if valores[i] == VALORES_VARIABLES:
                valores[i] = 0
                valores[i-1] += 1
            else:
                break

    while(valores[0] < 2):
        archivo.write("\n")
        linea = variables[0] + str(valores[0])
        for i in range(1, len(valores)):
            linea += "," + variables[i] + str(valores[i])

        iteraciones = random.randint(10, 30)
        for i in range(iteraciones-1):
            archivo.write(linea + "\n")
        archivo.write(linea)

        avanzar()
    archivo.close()




if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python generador_pruebas.py <num_variables>")
        exit()
    main(sys.argv[1])