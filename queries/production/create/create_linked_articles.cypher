MERGE (article:Article {title: $title})
WITH article
UNWIND $links_titles AS link_title
MERGE (to_article:Article {title: link_title})
CREATE (article)-[:LINKS_TO]->(to_article);