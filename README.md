# Data Structures portfolio-project

# Undirected Graph:
1. Implement the UndirectedGraph class, designed to support the following type of
graph: undirected, unweighted, no duplicate edges, no loops. Cycles are allowed.
2. Once completed, your implementation will include the following methods:
add_vertex(), add_edge()
remove_edge(), remove_vertex()
get_vertices(), get_edges()
is_valid_path(), dfs(), bfs()
3. Undirected graphs should be stored as a Python dictionary of lists where keys are
vertex names (strings) and associated values are Python lists with names (in any
order) of vertices connected to the 'key' vertex. 

# Directed Graph
1. Implement the DirectedGraph class, designed to support the following type of graph:
directed, weighted (positive edge weights only), no duplicate edges, no loops. Cycles
are allowed.
2. Once completed, your implementation will include the following methods:
add_vertex(), add_edge()
remove_edge(), get_vertices(), get_edges()
is_valid_path(), dfs(), bfs()
has_cycle()
3. Directed graphs should be stored as a two dimensional matrix, which is a list of lists
in Python. Element on the i-th row and j-th column in the matrix is the weight of
the edge going from the vertex with index i to the vertex with index j. If there is no
edge between those vertices, the value is zero. 