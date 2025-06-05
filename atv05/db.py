from neo4j import GraphDatabase

def conectar_neo4j():
    URI = "bolt://127.0.0.1:7687"  
    USER = "neo4j"
    PASSWORD = "4Vne3J-MecfuhD5t4KM"
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with GraphDatabase.driver(URI, auth=(USER, PASSWORD)) as driver:
        driver.verify_connectivity()
        print("Connection established.")
    return driver.session()