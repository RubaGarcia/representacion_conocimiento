#!/bin/bash

# Ruta del archivo a mostrar
archivo="/home/ubuntu/Escritorio/repos/representacion_conocimiento/practica4/tiempos.txt"

# Uso de watch para ejecutar 'cat' cada minuto
watch -n 60 cat "$archivo"
