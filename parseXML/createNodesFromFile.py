from itertools import filterfalse
from time import sleep

import neo4j.exceptions
from tqdm import tqdm
from neo4j import GraphDatabase

from queries_from_file import * # needed queries read from file

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "f9UPKfbus%Fjd&Tew&$6")
ARTICLES_PATH = 'wikipedia_data/parsed/articles.txt'

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
            session.run(delete_relationships)
            result = session.run(read_relationships_count)
            current_relationships = result.single()["C"]

        while current_nodes > 0:
            session.run(delete_nodes)
            result = session.run(read_nodes_count)
            current_nodes = result.single()["C"]

        session.run(drop_index)
        print("Database cleared.")


def create_new_index():
    print("Creating index...")

    with get_driver().session() as session:
        session.run(create_index)

    print("Index created.")


def get_lines_in_file(path: str):
    num_lines = 0
    with open(path, 'r') as file:
        for _ in file:
            num_lines += 1
    return num_lines

def insert_articles_from_file(path: str):
    print("Inserting articles from " + path + "...")

    # calculate number of lines for progress bar
    num_lines = get_lines_in_file(path)

    with open(path, 'r') as file:
        query = create_linked_articles
        for line in tqdm(file, total=num_lines):
            handle_line(line, query)


def handle_line(line, query: Query):
    components = line.split("->")
    title = components[0]
    links = components[1].split("|||")
    links.pop(0)  # remove '' that is created by splitting

    tries = 0
    success = False
    while tries < 2 and not success:
        success, tries = handle_query(links, query, success, title, tries)


def handle_query(links, query: Query, success, title, tries):
    with get_driver().session() as session:
        try:
            session.run(query, title=title, links_titles=links)
            success = True
        except neo4j.exceptions.DatabaseError:
            print(f"Failed to add entirety of article {title} containing links {links}")
        except (neo4j.exceptions.ServiceUnavailable, neo4j.exceptions.SessionExpired):
            print(f"Database connection lost, attempting reconnect...")
            sleep(60)
            test_connectivity()
        finally:
            tries += 1
    return success, tries


test_connectivity()
clear_database()
create_new_index()
insert_articles_from_file(ARTICLES_PATH)
