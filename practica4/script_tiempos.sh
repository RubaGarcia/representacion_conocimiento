#!/bin/bash

# Inicializa las variables
salida_generador=""
salida_chowLiu=""

# Itera entre 1 y 17
echo -e "num nodos\ttiempo" >> tiempos.txt
for i in {1..19}; do
    # Captura la salida de generador_pruebas
    salida_generador=$(python3 generador_pruebas.py "$i")

    # Captura la salida de chowLiu_tiempos
    salida_chowLiu=$(python3 chowLiu_tiempos.py)

    # Imprime la salida de generador_pruebas y chowLiu_tiempos separadas por un tabulador
    echo -e "$salida_generador\t$salida_chowLiu" >> tiempos.txt
done
