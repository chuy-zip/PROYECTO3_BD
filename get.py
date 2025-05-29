def get_puzzle(puzzle_name: str, driver) -> list:
    """
    Returns the pieces of a puzzle from the Neo4j database.
    
    Args:
        puzzle_name (str): Puzzle name to return.
        driver: Neo4j driver instance.

    Returns:
        list: A list containing the pieces of the puzzle.
    """
    records, summary, keys = driver.execute_query(
        "MATCH (p:Pieza) WHERE p.nombre_rompecabezas = $p_name RETURN p",
        p_name=puzzle_name,
        database="neo4j"
    )

    if not records:
        print(f"Puzzle '{puzzle_name}' not found in the database.")
        return None
    
    puzzle = []
    for record in records:
        puzzle.append({
            "id_num": record["p"]["id_num"],
            "nombre_rompecabezas": record["p"]["nombre_rompecabezas"],
            "faltante": record["p"]["faltante"],
            "material": record["p"]["material"],
            "marca": record["p"]["marca"],
            "tematica": record["p"]["tematica"],
            "forma": record["p"]["forma"],
            "rel_izq": -1,
            "rel_der": -1,
            "rel_arriba": -1,
            "rel_abajo": -1
        })

    print(f"Puzzle '{puzzle_name}' fetched from Neo4j database.\n")

    puzzle = get_piece_relations(puzzle, driver)
    return puzzle

def get_piece_relations(puzzle: list, driver) -> list:
    """
    Returns the relations of each piece in the puzzle.
    
    Args:
        puzzle (list): Puzzle pieces to get relations for.
        driver: Neo4j driver instance.

    Returns:
        list: A list containing the relations of each piece.
    """
    for pieza in puzzle:
        id_num = pieza["id_num"]
        records, summary, keys = driver.execute_query(
            "MATCH (p:Pieza)-[r:CONECTADO_A]->(q:Pieza) WHERE p.id_num = $id_num RETURN p, r, q",
            id_num=id_num,
            database="neo4j"
        )

        for record in records:
            piece = record["p"]
            relation = record["r"]
            related_piece = record["q"]

            print(f"{piece["id_num"]} - {relation["direccion"]} -> {related_piece["id_num"]}")
            
            if relation["direccion"] == "izquierda" and pieza["rel_izq"] == -1:
                pieza["rel_izq"] = related_piece["id_num"]
            elif relation["direccion"] == "derecha" and pieza["rel_der"] == -1:
                pieza["rel_der"] = related_piece["id_num"]
            elif relation["direccion"] == "arriba" and pieza["rel_arriba"] == -1:
                pieza["rel_arriba"] = related_piece["id_num"]
            elif relation["direccion"] == "abajo" and pieza["rel_abajo"] == -1:
                pieza["rel_abajo"] = related_piece["id_num"]

    print("Relations for each piece fetched from Neo4j database.\n")

    return puzzle