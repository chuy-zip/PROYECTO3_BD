import random
import json

def armar_rompecabezas(datos: json, pieza_inicio=None):
    # id_num -> nodo pieza
    piezas = {p['id_num']: p for p in datos}
    
    # data del rompecabezas
    primera_pieza = next(iter(piezas.values()))

    nombre = primera_pieza['nombre_rompecabezas']
    material = primera_pieza['material']
    marca = primera_pieza['marca']
    tematica = primera_pieza['tematica']
    forma = primera_pieza['forma']
    
    # Mostrar información general del rompecabezas
    print("\n+---- INFORMACIÓN DEL ROMPECABEZAS ----+")
    print(f"|  Nombre: {nombre}")
    print(f"|  Material: {material}")
    print(f"|  Marca: {marca}")
    print(f"|  Temática: {tematica}")
    print(f"|  Forma de las piezas: {forma}")
    print("+--------------------------------------+\n")

    # elegir una aleatoria
    if pieza_inicio is None:
        pieza_inicio = random.choice(list(piezas.keys()))
    
    print(f"INICIO en pieza #{pieza_inicio} -------------------------------------------+")
    
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
                        print(f"|  Conectar pieza #{pieza_relacionada} en el lado {direccion} de pieza #{pieza_actual}")
                        explorar_conexiones(pieza_relacionada, direccion, pieza_actual)
                else:
                    print(f"Advertencia: Pieza {pieza_relacionada} referenciada pero no existe en los datos")
    
    explorar_conexiones(pieza_inicio)
    print("FIN ----------------------------------------------------------+")


