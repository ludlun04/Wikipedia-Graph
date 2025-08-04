from neo4j import Query

def get_query_from_file(path: str):
    with open(path, 'r') as file:
        query = file.read()
    return Query(query)

create_index = get_query_from_file("queries/production/create/create_index.cypher")
create_linked_articles = get_query_from_file("queries/production/create/create_linked_articles.cypher")

delete_nodes = get_query_from_file("queries/production/delete/delete_nodes.cypher")
delete_relationships = get_query_from_file("queries/production/delete/delete_relationships.cypher")

read_nodes_count = get_query_from_file("queries/production/read/read_node_count.cypher")
read_relationships_count = get_query_from_file("queries/production/read/read_relationship_count.cypher")

drop_index = get_query_from_file("queries/production/delete/drop_index.cypher")