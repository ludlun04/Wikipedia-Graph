MATCH (node)
WITH node limit 1500000
DETACH DELETE node;