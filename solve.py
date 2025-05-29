import random
import json

def armar_rompecabezas(datos: json, pieza_inicio=None):
    # id_num -> nodo pieza
    piezas = {p['id_num']: p for p in datos}
    
    # elegir una aleatoria
    if pieza_inicio is None:
        pieza_inicio = random.choice(list(piezas.keys()))
    
    print(f"INICIO en pieza {pieza_inicio}")
    
    # registro de piezas ya visitadas
    visitadas = set()
    
    def explorar_conexiones(pieza_actual, direccion_padre=None, padre=None):
        if pieza_actual in visitadas:
            return
        visitadas.add(pieza_actual)
        
        for direccion, relacion in [
            ('IZQUIERDO', 'rel_izq'),
            ('DERECHO', 'rel_der'),
            ('ARRIBA', 'rel_arriba'),
            ('ABAJO', 'rel_abajo')
        ]:
            # no volver por donde vinimos :p
            if direccion_padre is not None and (
                (direccion_padre == 'IZQUIERDO' and direccion == 'DERECHO') or
                (direccion_padre == 'DERECHO' and direccion == 'IZQUIERDO') or
                (direccion_padre == 'ARRIBA' and direccion == 'ABAJO') or
                (direccion_padre == 'ABAJO' and direccion == 'ARRIBA')
            ): continue
                
            pieza_relacionada = piezas[pieza_actual][relacion]
            
            if pieza_relacionada != -1:
                if pieza_relacionada in piezas:
                    if piezas[pieza_relacionada]['faltante']:
                        print(f"Pieza faltante id #{pieza_relacionada}")
                    else:
                        print(f"Conectar pieza {pieza_relacionada} en el lado {direccion} de pieza {pieza_actual}")
                        explorar_conexiones(pieza_relacionada, direccion, pieza_actual)
                else:
                    print(f"Advertencia: Pieza {pieza_relacionada} referenciada pero no existe en los datos")
    
    explorar_conexiones(pieza_inicio)


# JONSON
datos_rompecabezas = None

with open('pterodactil_puzzle.json', 'r') as file:
    datos_rompecabezas = json.load(file)

# como llamar función
armar_rompecabezas(datos_rompecabezas)  # Para pieza aleatoria
# armar_rompecabezas(datos_rompecabezas, pieza_inicio=1)  # Para empezar en pieza 1