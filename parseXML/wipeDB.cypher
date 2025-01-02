MATCH (node)
WITH node limit 50000
DETACH DELETE node;