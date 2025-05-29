def ingresar_rompecabezas(piezas, driver):
    with driver.session() as session:
        # primero creacion de piezas
        for pieza in piezas:
            session.execute_write(crear_pieza, pieza)
        
        # luego la creacion de relaciones
        for pieza in piezas:
            session.execute_write(crear_relaciones, pieza)

def crear_pieza(tx, pieza):
    query = """
    MERGE (p:Pieza {id_num: $id_num, nombre_rompecabezas: $nombre_rompecabezas})
    ON CREATE SET
        p.faltante = $faltante,
        p.material = $material,
        p.marca = $marca,
        p.tematica = $tematica,
        p.forma = $forma
    """
    tx.run(query, 
           id_num=pieza['id_num'],
           nombre_rompecabezas=pieza['nombre_rompecabezas'],
           faltante=pieza['faltante'],
           material=pieza['material'],
           marca=pieza['marca'],
           tematica=pieza['tematica'],
           forma=pieza['forma'])

def crear_relaciones(tx, pieza):
    # Mapeo de relaciones a direcciones

    #nota: por la forma en la que modelamos el json las relaciones bidireccionales
    # se crean ya que para todas las piezas iteramos sobre las direcciones.
    direcciones = {
        'rel_izq': 'izquierda',
        'rel_der': 'derecha',
        'rel_arriba': 'arriba',
        'rel_abajo': 'abajo'
    }

    nombre_puzzle = pieza['nombre_rompecabezas']
    
    for rel_key, direccion in direcciones.items():
        pieza_destino = pieza[rel_key]
        if pieza_destino > 0:  # Solo crear relación si hay conexión
            query = query = """
            MATCH (p1:Pieza {id_num: $id_origen, nombre_rompecabezas: $nombre_puzzle})
            MATCH (p2:Pieza {id_num: $id_destino, nombre_rompecabezas: $nombre_puzzle})
            MERGE (p1)-[:CONECTADO_A {direccion: $direccion}]->(p2)
            """
            tx.run(query, 
                   id_origen=pieza['id_num'],
                   id_destino=pieza_destino,
                   nombre_puzzle=nombre_puzzle,
                   direccion=direccion)