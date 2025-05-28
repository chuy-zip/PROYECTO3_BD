from neo4j import GraphDatabase
import dotenv 
import os

def get_neo_driver():

    load_status = dotenv.load_dotenv()

    USER = os.getenv('NEO4J_USERNAME')
    PASSWORD = os.getenv('NEO4J_PASSWORD')

    URI = os.getenv('NEO4J_URI')
    AUTH = (USER, PASSWORD)

    if load_status is False:
        raise RuntimeError('Environment variables not loaded.')

    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()
    print("Connection established")

    return driver