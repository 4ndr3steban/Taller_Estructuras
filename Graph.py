class Graph:
    def __init__(self):
        self.graph = {}

    def print_graph(self):
        for vertex in self.graph:
            print(vertex, ':', self.graph[vertex])

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = {}
            return True
        return False

    def add_edge(self, v1, v2, weight):
        if v1 in self.graph and v2 in self.graph:
            self.graph[v1][v2] = weight
            self.graph[v2][v1] = weight

    def remove_edge(self, v1, v2):
        if v1 in self.graph and v2 in self.graph:
            del self.graph[v1][v2]
            del self.graph[v2][v1]

    def remove_vertex(self, vertex):
        if vertex in self.graph:
            for neighbor in self.graph[vertex]:
                del self.graph[neighbor][vertex]
            del self.graph[vertex]
            return True
        return False 

    def get_distance(self, v1, v2):
        if v1 in self.graph and v2 in self.graph:
            if v2 in self.graph[v1]:
                return self.graph[v1][v2]
        return float("inf")

    def dijkstra(self, origin, destination):
        distances = {vertex: float('inf') for vertex in self.graph}
        distances[origin] = 0
        
        previous = {vertex: None for vertex in self.graph}        
        visited = set()

        while len(visited) != len(self.graph):
            current_vertex = None
            min_distance = float('inf')

            for vertex in self.graph:
                if distances[vertex] < min_distance and vertex not in visited:
                    current_vertex = vertex
                    min_distance = distances[vertex]

            visited.add(current_vertex)
            print(visited)

            if current_vertex == destination:
                break

            for neighbor, weight in self.graph[current_vertex].items():
                distance = distances[current_vertex] + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_vertex

        best_route = []
        current_vertex = destination
        while current_vertex != origin:
            previous_vertex = previous[current_vertex]
            edge = (previous_vertex, current_vertex)
            best_route.insert(0, edge)
            current_vertex = previous_vertex

        return distances[destination], best_route
    
    def dfs(self, start_vertex, visited = None):
        if not visited:
            visited = []

        visited.append(start_vertex)
        
        for neighbor in self.graph[start_vertex]:   
            if neighbor not in visited:
                self.dfs(neighbor, visited)
        
        return visited
    
    def bfs(self, start_vertex):
        visited = []
        queue = [start_vertex]

        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.append(vertex)
                neighbors = self.graph[vertex]
                queue.extend(neighbors)

        return visited