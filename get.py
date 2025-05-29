def get_puzzle(puzzle_name: str, driver) -> dict:
    """
    Returns the pieces of a puzzle from the Neo4j database.
    
    Args:
        puzzle_name (str): Puzzle name to return.
        driver: Neo4j driver instance.

    Returns:
        dict: A dictionary containing the pieces of the puzzle.
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
            "rel_izq": record["p"]["rel_izq"],
            "rel_der": record["p"]["rel_der"],
            "rel_arriba": record["p"]["rel_arriba"],
            "rel_abajo": record["p"]["rel_abajo"]
        })

    print(f"Puzzle '{puzzle_name}' fetched from Neo4j database.")
    return puzzle