import os
import webbrowser

from Graph import Graph
from HashTable import Hast_table_sc
from haversine import haversine, Unit
from pyvis.network import Network 
from datetime import datetime

class Main:

    def __init__(self):
        self.historial = Hast_table_sc()
        self.grafo = Graph()
        self.data = None
        
        self.id_pedido = 0

        self.main()

    def inicializar_grafo(self):
        
        file = open("data.txt", "r", encoding="utf-8")

        # leer el archivo de lugares, se da formato a los datos y se guardan en un dict
        data = file.readlines()
        data = list(map(lambda x: x.rstrip().replace(" - ", ", ").split(", "), data))
        self.data = {x[0]: (float(x[1]),float(x[2])) for x in data}

        file.close()
        
        # agregamos la sucursal definida
        self.data["Universidad Nacional - Sede Volador"] = (6.261883148445439, -75.57720917341521) 

        # Agregar los vertices al grafo
        for loc in list(self.data.keys()):
            self.grafo.add_vertex(loc)

        # separar los nombres de lugar en locs y las cordenadas en cords
        locs = list(self.data.keys())
        cords = list(self.data.values())

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
            distances[loc] = distances[loc][:2]
            for neig in distances[loc]:
                self.grafo.add_edge(loc, neig[0], neig[1])

        #print(locations.dijkstra("Parque Arví", "Parque El Poblado"))

        """
        Aviso:

        lo hice asi por si depronto toca que cada nodo se conecte a mas nodos (no uno a uno)
        si despues confirmamos que no se solo es cambiar un pedacito pa que en el dict distances
        se guarde solo la menor distancia

        """

    def visualize_graph(self, filename):

        # creamos la lista de nodos, con un id especifico y el nombre del nodo
        nodes = {loc: idx for idx, loc in list(enumerate(self.grafo.graph))}

        # creamos la instancia de la red
        net = Network(notebook=True, cdn_resources="remote", height="1000px", width="100%")

        # agregamos todos los nodos
        net.add_nodes(list(nodes.values()), label=list(nodes.keys()))
        
        # creamos las conexiones entre los nodos
        for loc in nodes:
            for neighbor in self.grafo.graph[loc]:
                net.add_edge(nodes[loc], nodes[neighbor], 
                             value=self.grafo.graph[loc][neighbor], 
                             title=str(self.grafo.graph[loc][neighbor]))

        net.toggle_physics(True)

        # creamos el archivo html con la visualizacion del grafo
        filename = filename + ".html"
        net.show(filename)
        webbrowser.open('file://' + os.path.realpath(filename))


    def agregar_pedido(self):

        # creamos la instancia de cada pedido como un diccionario
        pedido = {}

        # pedimos la informacion correspondiente de cada pedido

        pedido["ubicacion"] = input("Ingrese el nombre del destino: ")

        while True:
            coords = input("Ingrese las coordenadas del pedido en formato (lat, lon): ").split(", ")
            if len(coords) == 2:
                try:
                    coords = tuple(map(lambda x: float(x), coords))
                    pedido["coordenadas"] = coords
                    break
                except:
                    continue

        pedido["descripcion"] = input("Ingrese la descripcion de su pedido: ")

        pedido["fecha"] = datetime.now()
        pedido["estado"] = "sin entregar"
        pedido["mensajero"] = "sin asignar"

        #print("Pedido agregado con exito con id: ", self.id_pedido, "\n")
        
        # agregamos el pedido a la tabla hash del historial
        self.historial.set_item(pedido["ubicacion"], pedido)
        #self.id_pedido += 1

        # agregamos la ubicacion del pedido al grafo 
        self.grafo.add_vertex(pedido["ubicacion"])

        # hallamos el nodo con el cual se conectará esta nueva ubicacion

        # separar los nombres de lugar en locs y las cordenadas en cords
        locs = list(self.data.keys())
        cords = list(self.data.values())

        # para guardar las distancias de un nodo al resto de nodos
        distances = {pedido["ubicacion"]: []} 

        for idx in range(len(locs)):
            # calcula la distancia en km (formula de haversine me la recomendo el juanjo y yo confio)
            dist = int(haversine(cords[idx], pedido["coordenadas"], Unit.KILOMETERS) * 1000)
            # se agrega la distancia como valor al key(nodo actual) (distancia a cada nodo)
            distances[pedido["ubicacion"]].append((locs[idx], dist))

        # se ordena las distancias a las demas y se toma la primera
        distances[pedido["ubicacion"]].sort(key = lambda x: x[1])
        distances[pedido["ubicacion"]] = distances[pedido["ubicacion"]][:2]
        for neig in distances[pedido["ubicacion"]]:
            self.grafo.add_edge(pedido["ubicacion"], neig[0], neig[1])

        # actualizamos el diccionario con los datos de ubicaciones y coordenadas
        self.data[pedido["ubicacion"]] = pedido["coordenadas"]

    def enviar_pedido(self):

        while True:
            pedido = input("Ingrese la ubicación exacta del pedido a enviar: ")
            if pedido in self.historial.keys():
                ruta = self.grafo.dijkstra("Universidad Nacional - Sede Volador", pedido)
                break
            else:
                print("Ubicación inexistente o no ingresada correctamente, intentelo nuevamente")
                continue
                    

        print("\nPedido enviado correctamente\n")
        print("La ruta que seguirá el mensajero es la siguiente:")
        print(ruta[1])
        print("La distancia que recorrerá será:")
        print(ruta[0], "metros")

        hist_pedido = self.historial.get_item(pedido)
        hist_pedido["estado"] = "Entregado"
        self.historial.remove_item(pedido)
        self.historial.set_item(hist_pedido["ubicacion"], hist_pedido)

        self.grafo.remove_vertex(pedido)
        del self.data[pedido]

        locs = list(self.data.keys())
        cords = list(self.data.values())

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
            distances[loc] = distances[loc][:2]
            for neig in distances[loc]:
                self.grafo.add_edge(loc, neig[0], neig[1])

    def consultar_pedidos(self):
        hist = self.historial.items()
        hist = list(filter(lambda x: x[1]["estado"] == "sin entregar", hist))
        if len(hist) > 0:
            print(hist)
        else:
            print("Aun no hay peididos")

    def consultar_enviados(self):
        hist = self.historial.items()
        hist = list(filter(lambda x: x[1]["estado"] == "Entregado", hist))
        if len(hist) > 0:
            print(hist)
        else:
            print("Aun no hay peididos entregados")
        

    def main(self):

        self.inicializar_grafo()

        while True:
            print("Representación de red de mensajería mediante grafos")
            print("Por medio de este menú puede acceder a las diferentes funciones del grafo\n")

            print("0. Terminar ejecución")
            print("1. Generar representación grafica del grafo")
            print("2. Generar un nuevo pedido")
            print("3. Mostrar historial de lugares con pedidos")
            print("4. Consultar los detalles de pedidos en base a ubicacion")
            print("5. Consultar los detalles de pedidos NO entregados")
            print("6. Consultar los detalles de pedidos entregados")
            print("7. Enviar un pedido")
            
            opcion = int(input("\nIngrese el numero de la opción deseada: "))
            if opcion == 0:
                break
            elif opcion == 1:
                self.visualize_graph("grafo")
            elif opcion == 2:
                self.agregar_pedido()
            elif opcion == 3:
                print("\n", self.historial.keys())
            elif opcion == 4:
                ubicacion = input("\nIngrese el nombre de la ubicación exacta: ")
                pedido = self.historial.get_item(ubicacion)
                for key in pedido:
                    print(f"{key}: {pedido[key]}")
            elif opcion == 5:
                self.consultar_pedidos()
            elif opcion == 6:
                self.consultar_enviados()
            elif opcion == 7:
                self.enviar_pedido()

            print()

if __name__ == '__main__':
    
    Main()