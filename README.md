# About the project
The idea of this project is to represent the relational structure of all Wikipedia articles in a graph data structure.
This enables us to quickly find the optimal path to navigate between given articles as efficiently as possible.
I got this idea from a youtube-video where people competed against each other,
seeing who could navigate between two unrelated topics on Wikipedia the fastest using only links within the articles.
When I learned about the graph data structure in the course [IDATA2302 - Algorithms and Data Structures](https://www.ntnu.edu/studies/courses/IDATA2302/2024#tab=omEmnet),
I knew it could be applied to solve this problem.

Using a publically available download of the entirety of english Wikipedia, and the graph database management system [Neo4j](https://neo4j.com/), this problem has been solved.

# Prerequisites
- Neo4j must be running locally, the easiest way is using docker compose with the provided compose.yml file.
- Wikipedia must be downloaded as an XML-file named enwiki.xml in the 'raw' directory of the project.

# Use
- To extract relevant data from the XML-file, run 'parse_wikipedia.py'.
- To insert this data into the database, run 'parsed_to_db.py'.
- To view the database and run queries, visit http://localhost:7474/browser/preview/ to access the local Neo4j webserver.
- To see the fastest path(s) between two given articles, use:
```cypher
MATCH p = allShortestPaths((from:Article)-[:LINKS_TO*]->(to:Article))
WHERE from.title = "Norway" AND to.title = "Atheris hispida"
RETURN [n IN nodes(p) | n.title] AS stops

```

# Known issues
- Some parts of articles that are not links, such as lists of coordinates, get interpreted as links. This results in such articles not being included in the final graph.
- The connectivity to the database becomes unstable after it has been connected for a while, which necessitates having to wait and reconnect.
- Inserting into the database takes a long time (22 hours for me). This is with indexing implemented and working.

# Future work
The current solution is very fragmented and requires the user to do a lot of manual tasks.
I plan to make the solution more streamlined, such that the user can interact with a single interface to accomplish everything.
I also want to publically host a website so anyone can see the fastest path without having to run the solution locally.
