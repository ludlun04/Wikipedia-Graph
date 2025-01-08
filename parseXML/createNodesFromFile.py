from itertools import filterfalse
from time import sleep

import neo4j.exceptions
from tqdm import tqdm
from neo4j import GraphDatabase
import psutil

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "f9UPKfbus%Fjd&Tew&$6")
TITLES_PATH = 'parsed/articles.txt'
CONNECTIONS_PATH = 'parsed/links.txt'

query_group_size = 100


def get_driver():
    return GraphDatabase.driver(URI, auth=AUTH)


def test_connectivity():
    print("Checking connection to database...")
    with get_driver() as driver:
        driver.verify_connectivity()
    print("Connection ok.")


def clear_database():
    print("Clearing database...")
    with get_driver().session() as session:
        current_relationships = 1
        current_nodes = 1

        while current_relationships > 0:
            session.run("MATCH (n1)-[r:LINKS_TO]->(n2) WITH r LIMIT 150000 DETACH DELETE r;")
            result = session.run("MATCH (n1)-[r:LINKS_TO]->(n2) WITH r RETURN COUNT(r) AS C")
            current_relationships = result.single()["C"]

        while current_nodes > 0:
            session.run("MATCH (node) WITH node LIMIT 150000 DETACH DELETE node;")
            result = session.run("MATCH (node) RETURN COUNT(node) AS C")
            current_nodes = result.single()["C"]
        session.run("DROP INDEX title_index IF EXISTS")
        print("Database cleared.")


def create_constraints():
    print("Creating constraints...")

    with get_driver().session() as session:
        session.run("CREATE INDEX title_index FOR (a:Article) ON a.title")

    print("Constraints created.")


def insert_articles_from_file(path: str):
    print("Inserting articles from " + path + "...")

    num_lines = 0

    # calculate number of lines for progress bar
    with open(path, 'r') as file:
        for _ in file:
            num_lines += 1

    with open(path, 'r') as file:

        query = """
                MERGE (article:Article {title: $title})
                WITH article
                UNWIND $links_titles AS link_title
                MERGE (to_article:Article {title: link_title})
                CREATE (article)-[:LINKS_TO]->(to_article)
                """

        for line in tqdm(file, total=num_lines):
            components = line.split("->")
            title = components[0]
            links = components[1].split("|||")
            links.pop(0)  # remove '' that is created by splitting

            # print(title)
            # print(links)

            tries = 0
            success = False
            while tries < 2 and not success:
                with get_driver().session() as session:
                    try:
                        session.run(query, title=title, links_titles=links)
                        success = True
                    except neo4j.exceptions.DatabaseError:
                        print(f"Failed to add entirety of article {title} containing links {links}")
                    except neo4j.exceptions.ServiceUnavailable:
                        print(f"Database connection lost, attempting reconnect...")
                        test_connectivity()
                    finally:
                        tries += 1


test_connectivity()
clear_database()
create_constraints()
insert_articles_from_file(TITLES_PATH)
