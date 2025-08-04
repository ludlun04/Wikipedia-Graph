MERGE (Test1:Article)
MERGE (Test2:Article {content: 'Article 2 content'})
MERGE (Test1)-[:LINKS_TO]->(Test2);