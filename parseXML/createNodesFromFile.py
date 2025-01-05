from time import sleep

from neo4j import GraphDatabase
from tqdm import tqdm
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
        current_nodes = 1
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

def insert_articles_from_file(path):
    print("Inserting articles from " + path + "...")

    num_lines = 0

    # calculate number of lines for progress bar
    with open(path, 'r') as file:
        for _ in file:
            num_lines += 1

    with open(path, 'r') as file:
        for line in tqdm(file, total=num_lines):
            components = line.split("->")
            title = components[0]
            links = components[1].split("|||")

            with get_driver().session() as session:
                query = """
                MERGE (article:Article {title: $title})
                WITH article
                UNWIND $links_titles AS link_title
                MERGE (to_article:Article {title: link_title})
                CREATE (article)-[:LINKS_TO]->(to_article)
                """
                session.run(query, title=title, links_titles=links)




def get_connections_from_file(path, from_line):
    print("Getting connections from " + path + "...")
    connections_from = []
    connections_to = []
    connections = (connections_from, connections_to)

    # used to check available memory at intervals, checking each iteration hurts performance a lot
    # an interval of 1000000 is about 400MB more memory used between each interval in my testing
    # computer may freeze if out of memory
    interval = 1000000
    mem_limit = 1024 * 1024 * 3000  # 3000MB

    with open(path, 'r') as file:
        for current_line_number, line in tqdm(enumerate(file, start=from_line)):

            if current_line_number % interval == 0:
                sleep(5)  # psutil does not provide real time readings, need to wait a bit to ensure reliable readings

                available = psutil.virtual_memory().free
                if available < mem_limit:
                    print(
                        f"Not enough memory to parse entire file in one go. {len(file.readlines()) - current_line_number} lines left")
                    return connections, from_line

            articles = line.split("->")

            article_from = articles[0]
            article_from = article_from.replace("\n", "")  # avoid newline
            article_to = articles[1]
            article_to = article_to.replace("\n", "")  # avoid newline

            connections[0].append(article_from)
            connections[1].append(article_to)

    print(f"Got {len(connections)} connections from file")
    return connections, 0


def add_titles_to_database(titles):
    print("Adding titles to database...")
    with get_driver().session() as session:
        query = "UNWIND $titles as title CREATE (:Article {title: title})"
        for i in tqdm(range(1, len(titles), query_group_size)):
            group = titles[i: i + query_group_size]
            session.run(query, titles=group)
    print("Titles added to database.")


def add_connections_to_database(connections):
    print("Adding connections to database...")
    with get_driver().session() as session:
        query = """
        UNWIND $from_articles AS from_title
        UNWIND $to_articles AS to_title
        MERGE (from_article:Article {title: from_title})
        MERGE (to_article:Article {title: to_title})
        MERGE (from_article)-[:LINKS_TO]->(to_article)
        """
        # print(f"UNWIND $connections as tuple CREATE ({connections[0][0]})-[:LINKS_TO]->({connections[0][1]}) SET A1 = tuple[0], A2 = tuple[1]")
        for i in tqdm(range(1, len(connections), query_group_size)):
            from_articles = connections[0][i: i + query_group_size]
            to_articles = connections[1][i: i + query_group_size]
            session.run(query, from_articles=from_articles, to_articles=to_articles)
        print("added one connection")
    print("Connections added to database.")


def insert_nodes_from_file():
    titles = get_titles_from_file(TITLES_PATH)
    add_titles_to_database(titles)


def insert_connections_from_file():
    from_line = 1
    while from_line != 0:
        connections, from_line = get_connections_from_file(CONNECTIONS_PATH, from_line)
        add_connections_to_database(connections)


test_connectivity()
clear_database()
create_constraints()
insert_articles_from_file(TITLES_PATH)
