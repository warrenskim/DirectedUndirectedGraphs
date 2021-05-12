# Course: CS261 - Data Structures
# Author: Warren Kim
# Assignment: Portfolio Project
# Description: Implement an UndirectedGraph class by completing the provided
#   skeleton code, while supporting the following types of graphs:
#   undirected, unweighted, no duplicated edges, no loops; cycles allowed.


class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """
        if v not in self.adj_list:
            self.adj_list[v] = []
        
    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """
        if u == v:
            return
        self.add_vertex(u)
        self.add_vertex(v)
        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)
        if u not in self.adj_list[v]:
            self.adj_list[v].append(u)

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """
        if u not in self.adj_list or v not in self.adj_list:
            return
        # With the way add_edge() is set up, we can use one comparison
        #   to remove from both lists
        if v in self.adj_list[u]:
            self.adj_list[u].remove(v)
            self.adj_list[v].remove(u)

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        if v in self.adj_list:
            # For every key in the dictionary:
            for key in self.adj_list:
                # if that key's list contains an edge to v, remove.
                if v in self.adj_list[key]:
                    self.adj_list[key].remove(v)
            del self.adj_list[v]

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        vertices_list = []
        for vertex in self.adj_list:
            vertices_list.append(vertex)
        return vertices_list

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        edges_list = []
        for vertex in self.adj_list:
            for edge in self.adj_list[vertex]:
                # We just need to make sure the reverse tuple
                #   is not already in our list
                if (edge, vertex) not in edges_list:
                    edges_list.append((vertex, edge))
        return edges_list

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise

        We should set this up by checking if the first vertex is in
        the graph. Then, the second vertex should be checked in the first
        vertex's edge list. Then, the third vertex should be checked in
        the second vertex's edge list, and so on.

        This may require two variables -- one to hold the "current" vertex
        and one to hold the "previous" OR "next" vertex.
        """
        i = 1
        for vertex in path:
            # We put this comparison first to ensure that every
            #   vertex is in the graph
            if vertex not in self.adj_list:
                return False
            # We put this comparison before the next one to avoid
            #   reaching an unreachable point in the provided path
            if i == len(path):
                return True
            if path[i] not in self.adj_list[vertex]:
                return False
            i += 1
        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        if v_start not in self.adj_list:
            return []
        visited = []
        stack = [v_start]
        self.rec_dfs(v_end, visited, stack)
        return visited

    def rec_dfs(self, v_end, visited: [], stack: []):
        """
        Helper method for dfs()
        """
        # Here, we establish the popped vertex, as well as make
        #   comparisons to ensure that we haven't reached the
        #   end of our search.
        if len(stack) == 0:
            return
        popped = stack.pop()
        # Add every reachable vertex to the popped vertex to a
        #   temporary list. This way, we can sort by min or max
        #   if needed.
        temp_list = []
        if popped not in visited:
            visited.append(popped)
            for edge in self.adj_list[popped]:
                temp_list.append(edge)
        # Since we're using a stack to track the vertices,
        #   we need to add in order by maximum value so that we can
        #   POP off the min value and evaluate that next
        while temp_list:
            stack.append(max(temp_list))
            temp_list.remove(max(temp_list))
        # Checking if end vertex is in visited list
        if v_end in visited:
            return
        # Call itself again recursively
        self.rec_dfs(v_end, visited, stack)

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        if v_start not in self.adj_list:
            return []
        visited = []
        queue = [v_start]
        self.rec_bfs(v_end, visited, queue)
        return visited

    def rec_bfs(self, v_end, visited: [], queue: []):
        """
        Helper method for bfs()
        """
        # Here, we establish the popped vertex, as well as make
        #   comparisons to ensure that we haven't reached the
        #   end of our search.
        if len(queue) == 0:
            return
        dequeued = queue[0]
        del queue[0]
        # Add every reachable vertex to the popped vertex to a
        #   temporary list. This way, we can sort by min or max
        #   if needed.
        temp_list = []
        if dequeued not in visited:
            visited.append(dequeued)
            for edge in self.adj_list[dequeued]:
                temp_list.append(edge)
        # Since we're using a queue to track the vertices,
        #   we need to add in order by minimum value so that we can
        #   dequeue the min value and evaluate that next
        while temp_list:
            queue.append(min(temp_list))
            temp_list.remove(min(temp_list))
        # Checking if our end vertex is in the list
        if v_end in visited:
            return
        # Call itself again recursively
        self.rec_bfs(v_end, visited, queue)

    def reachable_vertices(self, v_start) -> []:
        """
        Find reachable vertices from a vertex
        """
        stack = [v_start]
        reachable = []
        self.rec_reachable_vertices(reachable, stack)
        return reachable

    def rec_reachable_vertices(self, reachable: [], stack: []):
        """
        Helper method for dfs()
        """
        # Here, we establish the popped vertex, as well as make
        #   comparisons to ensure that we haven't reached the
        #   end of our search.
        if len(stack) == 0:
            return
        popped = stack.pop()
        if popped not in reachable:
            reachable.append(popped)
        # Using a stack to append each vertex
            for edge in self.adj_list[popped]:
                stack.append(edge)
        # Recall recursively
        self.rec_reachable_vertices(reachable, stack)


# Tests:
if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')