######################################################
#       LABORATORIO 3 - BASE DE DATOS 2
#       AUTORES:
#           Eunice Mata......21231
#           Ricardo Chuy.....221007
#           Hector Penedo....22217
#           Pedro Pablo
#           Chen
#           Gustavo
######################################################

from connection import get_neo_driver
from create import ingresar_rompecabezas
import json

driver = get_neo_driver()

salir = False

while not salir:
    print("\n--- Menú Principal ---")
    print("1. Insertar un nuevo rompecabezas desde archivo JSON")
    print("2. Resolver un rompecabezas existente")
    print("3. Salir")

    opcion = input("Seleccione una opción (1-3): ").strip()

    if opcion == "1":
        archivo = input("Ingrese el nombre del archivo JSON (ej. 'puzzle1.json'): ").strip()
        with open(archivo, 'r', encoding='utf-8') as f:
            piezas = json.load(f)

        ingresar_rompecabezas(piezas, driver)

        print(f"Rompecabezas '{piezas[0]['nombre_rompecabezas']}' insertado correctamente con {len(piezas)} piezas.")
    
    if opcion == "2":
        puzzle_name = input("Ingrese el nombre del puzzle que desea resolver: ").strip()
        print(f"Solución del rompecabezas: '{puzzle_name}'.")
        print("pendiente")

    if opcion == "3":
        salir = True