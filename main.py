from graph import Graph
from haversine import haversine, Unit

locations = Graph()

file = open("data.txt", "r", encoding="utf-8")

# leer el archivo de lugares, se da formato a los datos y se guardan en un dict
data = file.readlines()
data = list(map(lambda x: x.rstrip().replace(" - ", ", ").split(", "), data))
data = {x[0]: (float(x[1]),float(x[2])) for x in data}

#print(data)

# Agregar los vertices al grafo
for loc in list(data.keys()):
    locations.add_vertex(loc)

# separar los nombres de lugar en locs y las cordenadas en cords
locs = list(data.keys())
cords = list(data.values())

# para guardar las distancias de un nodo al resto de nodos
distances = {}

# calcular las distancias de un nodo al resto de nodos
for idx in range(len(locs)-1):
    # se agrega el nodo actual como key al dict distances
    distances[locs[idx]] = []

    for next in range(idx+1, len(locs)):

        # calcula la distancia en km (formula de haversine me la recomendo el juanjo y yo confio)
        dist = int(haversine(cords[idx], cords[next], Unit.KILOMETERS) * 1000)

        # se agrega la distancia como valor al key(nodo actual) (distancia a cada nodo)
        distances[locs[idx]].append((locs[next], dist))


for loc in distances:
    # en cada nodo se ordena las distancias a las demas y se toma la primera
    distances[loc].sort(key = lambda x: x[1])
    distances[loc] = distances[loc][:1]
    for neig in distances[loc]:
        locations.add_edge(loc, neig[0], neig[1])

print(locations.dijkstra("Parque Arví", "Parque El Poblado"))

"""
Aviso:

lo hice asi por si depronto toca que cada nodo se conecte a mas nodos (no uno a uno)
si despues confirmamos que no se solo es cambiar un pedacito pa que en el dict distances
se guarde solo la menor distancia

"""