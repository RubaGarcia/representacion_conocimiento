#write in file
import random
import sys





def generar_letras_no_repetidas(num):
    letras = "abcdefghiJKLMNOpqrstuvwxyzÁÉÍÓÚáéíóúÜüÇçßàèìòùãõñĀāĒēĪīŌōŪū¿¡_!@#$%^&*-=+<>?/"
    letras=letras.lower()
    letras_no_repetidas = random.sample(letras, min(num, len(letras)))
    return letras_no_repetidas



n = int(sys.argv[1])

if len(sys.argv) >= 2:
    f = open("base_tablas_" + str(sys.argv[1]) + ".txt", "w")
    #quiero generar un array con n letras no repetidas
    

    letras = generar_letras_no_repetidas(n)

    for i in letras[:-1]:
        f.write(i + "2,")
    f.write(letras[-1] + "2\n")


    f.write(str(letras[0]) + "0:0.5\n" +
        str(letras[0]) + "1:0.5\n")

    for i in range(1, len(letras)):
        f.write(str(letras[i]) + "0," + str(letras[i-1]) + "0:0.5\n" +
            str(letras[i]) + "1," + str(letras[i-1]) + "0:0.5\n" +
            str(letras[i]) + "0," + str(letras[i-1]) + "1:0.5\n" +
            str(letras[i]) + "1," + str(letras[i-1]) + "1:0.5\n")
        
    
   

    for i in range(len(letras)-1):
        f.write(str(letras[i].upper())+",")
    f.write("\n")    
    f.write("None\n")
else:
    print("Error: no se ha introducido el numero de la base")
    exit()