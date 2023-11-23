#!/bin/bash

touch resultados.txt
# Nombre del archivo de salida
output_file="resultados.txt"

# Bucle de 0 al 7
for i in {0..6}; do
    # Llamar al programa Python con el parámetro del iterador
    echo "Ejecutando fichero $i ..." >> $output_file

    { time python3 inferencia_probabilistica_exacta.py $i; } 2>> $output_file

    # Imprimir un separador en el archivo de salida
    
    echo "------------------------" >> $output_file
done

echo "Proceso completado. Los resultados se han guardado en $output_file"
