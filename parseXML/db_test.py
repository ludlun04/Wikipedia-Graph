from neo4j import GraphDatabase, Query

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "f9UPKfbus%Fjd&Tew&$6")

def get_driver():
    return GraphDatabase.driver(URI, auth=AUTH)

def test_connectivity():
    with get_driver() as driver:
        driver.verify_connectivity()

def create_constraints():
    with open('queries/production/create/create_constraints.cypher', 'r') as file:
        query = file.read()
    with get_driver() as driver:
        driver.execute_query(Query(query))

def insert_sample_data():
    with open('queries/testing/wikipediaSampleNodes.cypher', 'r') as file:
        query = file.read()
    with get_driver() as driver:
        driver.execute_query(query)

test_connectivity()
create_constraints()
insert_sample_data()


