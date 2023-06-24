from Graph import Graph

nodos_base = {}

with open("data.txt", "r") as f:
    for dato in f:
        lugar, coordenadas = dato.split(" - ")
        coordenadas = list(map(lambda x: float(x), coordenadas[:-1].split(", ")))
        nodos_base[lugar] = coordenadas

graph = Graph()

for nodo in nodos_base:
    graph.add_vertex(nodo)

graph.print_graph()