# Course: CS261 - Data Structures
# Author: Warren Kim
# Assignment: Portfolio Project
# Description: Implement a DirectedGraph class by completing the provided
#   skeleton code while supporting the following types of graphs:
#   directed, (positive-)weighted, no duplicate edges, no loops; cycles allowed.

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        TODO: Write this implementation
        """
        if self.v_count > 0:
            # Adding an extra value for each existing vertex list
            for vertex_list in self.adj_matrix:
                vertex_list.append(0)
        # Adding the new vertex list
        self.adj_matrix.append([])
        self.v_count += 1
        # Giving that vertex list the appropriate number of values
        for i in range(self.v_count):
            self.adj_matrix[-1].append(0)
        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        TODO: Write this implementation
        """
        if src < 0 or src > self.v_count-1:
            return
        if dst < 0 or dst > self.v_count-1:
            return
        if src == dst:
            return
        # As long as the weight is > 0, it's an edge we can add.
        if weight <1:
            return
        self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        TODO: Write this implementation
        """
        if src < 0 or src > self.v_count-1:
            return
        if dst < 0 or dst > self.v_count-1:
            return
        if src == dst:
            return
        # Being sure to remove the weight in only one direction
        self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        TODO: Write this implementation
        """
        vertices = []
        index = 0
        for vertex in self.adj_matrix:
            vertices.append(index)
            index+=1
        return vertices

    def get_edges(self) -> []:
        """
        TODO: Write this implementation
        """
        edges = []
        src_index = 0
        dst_index = 0
        # Because length of matrix = number of verteices in matrix
        while src_index < len(self.adj_matrix):
            # Because length of matrix = number of indexes in vertex list
            while dst_index < len(self.adj_matrix):
                # Adding any weight > 0, meaning it's an edge
                weight = self.adj_matrix[src_index][dst_index]
                if weight > 0:
                    edges.append((src_index, dst_index, weight))
                dst_index += 1
            # Increasing src_index and resetting dst_index
            src_index += 1
            dst_index = 0
        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        TODO: Write this implementation
        For this method, it's easiest to consider that the provided path
        gives us the index of each vertex. We can use that to check if an edge
        exists at the appropriate place in the matrix.
        """
        index = 1
        while index < len(path):
            src = path[index-1]
            dst = path[index]
            # As long as the weight is > 0, we're able to verify
            #   that an edge exists
            if self.adj_matrix[src][dst] == 0:
                return False
            index += 1
        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        TODO: Write this implementation
        """
        if v_start < 0 or v_start > len(self.adj_matrix)-1:
            return
        visited = []
        stack = [v_start]
        self.rec_dfs(v_end, visited, stack)
        return visited

    def rec_dfs(self, v_end, visited: [], stack: []):
        """
        Helper method for dfs()
        """
        if len(stack) == 0:
            return
        popped = stack.pop()

        temp_list = []
        if popped not in visited:
            visited.append(popped)
            i = 0
            while i < len(self.adj_matrix):
                edge_weight = self.adj_matrix[popped][i]
                if edge_weight > 0:
                    temp_list.append(i)
                i+=1
        while temp_list:
            stack.append(max(temp_list))
            temp_list.remove(max(temp_list))

        if v_end in visited:
            return
        self.rec_dfs(v_end, visited, stack)

    def bfs(self, v_start, v_end=None) -> []:
        """
        TODO: Write this implementation
        """
        if v_start < 0 or v_start > len(self.adj_matrix) - 1:
            return
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
            i = 0
            while i < len(self.adj_matrix):
                edge_weight = self.adj_matrix[dequeued][i]
                if edge_weight > 0:
                    temp_list.append(i)
                i += 1
        # Since we're using a queue to track the vertices,
        #   we need to add in order by minimum value so that we can
        #   dequeue the min value and evaluate that next
        while temp_list:
            queue.append(min(temp_list))
            temp_list.remove(min(temp_list))
        # Check if end value is in our visited list
        if v_end in visited:
            return
        # Call itself again recursively
        self.rec_bfs(v_end, visited, queue)

    def has_cycle(self):
        """
        Determine if there's a cycle
        """
        number_of_vertices = len(self.get_vertices())
        number_of_edges = len(self.get_edges())
        if number_of_edges != number_of_vertices-1:
            return True
        return False


# Tests:
if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


