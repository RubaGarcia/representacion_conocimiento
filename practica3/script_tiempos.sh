#!/bin/bash

touch resultados.txt
# Nombre del archivo de salida
output_file="resultados.txt"

# Bucle de 0 al 7
for i in {1..62}; do
    # Llamar al programa Python con el parámetro del iterador
    echo "Ejecutando fichero $i ..." 

    python3 creacion_base.py $i  


    python3 inferencia_probabilistica_exacta.py $i >> $output_file
    # Imprimir un separador en el archivo de salida
    

    #echo "------------------------" >> $output_file
done

echo "Proceso completado. Los resultados se han guardado en $output_file"
