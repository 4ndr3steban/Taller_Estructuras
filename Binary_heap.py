class MinBinaryHeap():
    
    def __init__(self):

        # inicializamos el index y la lista con longitud 1
        # para operar desde el indice 1 de forma mas sencilla

        self.heap = [0]
        self.n = 0

    # metodo para comprobar si el heap esta vacio
    def isEmpty(self):
        return self.n == 0
    
    # metodo para comprobar si un elemento en una posicion es mayor que otro
    def greater(self, a, b):
        return self.heap[a] > self.heap[b]
    
    # metodo para intercambiar los elementos de dos posiciones
    def exch(self, a , b):
        self.heap[a], self.heap[b] = self.heap[b], self.heap[a]

    # caso en el que el hijo es menor que el padre
    def swim(self, k):
        # mientras la llave k (index lista) es mayor que el index del root y 
        # mientras el padre es menor que el hijo.
        while(k > 1 and self.greater(k // 2, k)):
            # el padre de k es k // 2
            self.exch(k//2, k)
            k = k//2

    # metodo para manejar la insercion en la lista
    # se agrega el elemento al final, y se sube hasta que sea necesario
    def insert(self, x):
        self.n += 1
        self.heap.append(x)
        self.swim(self.n) 


    # metodo para manejar el caso en el que el valor de un elemento en un indice
    # padre es mayor que un elemento en un indice hijo
    # intercambiar con el hijo mas pequeño hasta que el orden del heap sea el 
    # correcto
    def sink(self, k):
        # mientras no se llegue al final de la lista

        while 2*k <= self.n:
            j = 2*k

            # seleccionar el indice hijo menor (entre los dos hijos)
            # los indices de esos nodos son 2*k, 2*k+1
            if j < self.n and self.greater(j, j+1): 
                j += 1

            # si el padre no es mayor que el hijo, entonces salir
            if not self.greater(k, j): 
                break

            # intercambiar 
            self.exch(k, j)
            k = j

    def delMin(self):

        if self.isEmpty():
            return None

        min = self.heap[1]
        
        # intercambiar el primer y ultimo elemento
        self.exch(1, self.n)
        self.n -= 1
        self.heap.pop()

        # hundir el elemento que se intercambio hasta que el heap este en orden
        self.sink(1)

        # eliminar el minimo (que esta al final al ser intercambiado)
        return min
    
class MaxBinaryHeap():
        
    def __init__(self):

        # inicializamos el index y la lista con longitud 1
        # para operar desde el indice 1 de forma mas sencilla

        self.heap = [0]
        self.n = 0

    # metodo para comprobar si el heap esta vacio
    def isEmpty(self):
        return self.n == 0
    
    # metodo para comprobar si un elemento en una posicion es menor que otro
    def less(self, a, b):
        return self.heap[a] < self.heap[b]
    
    # metodo para intercambiar los elementos de dos posiciones
    def exch(self, a , b):
        self.heap[a], self.heap[b] = self.heap[b], self.heap[a]

    # caso en el que el hijo es mayor que el padre
    def swim(self, k):
        # mientras la llave k (index lista) es mayor que el index del root y 
        # mientras el padre es mayor que el hijo.
        while(k > 1 and self.less(k // 2, k)):
            # el padre de k es k // 2
            self.exch(k//2, k)
            k = k//2

    # metodo para manejar la insercion en la lista
    # se agrega el elemento al final, y se sube hasta que sea necesario
    def insert(self, x):
        self.n += 1
        self.heap.append(x)
        self.swim(self.n) 


    # metodo para manejar el caso en el que el valor de un elemento en un indice
    # padre es menor que un elemento en un indice hijo
    # intercambiar con el hijo mas grande hasta que el orden del heap sea el 
    # correcto
    def sink(self, k):
        # mientras no se llegue al final de la lista

        while 2*k <= self.n:
            j = 2*k

            # seleccionar el indice hijo mayor (entre los dos hijos)
            # los indices de esos nodos son 2*k, 2*k+1
            if j < self.n and self.less(j, j+1): 
                j += 1

            # si el padre no es menor que el hijo, entonces salir
            if not self.less(k, j): 
                break

            # intercambiar 
            self.exch(k, j)
            k = j

    def delMax(self):

        if self.isEmpty():
            return None

        max = self.heap[1]
        
        # intercambiar el primer y ultimo elemento
        self.exch(1, self.n)
        self.n -= 1
        self.heap.pop()

        # hundir el elemento que se intercambio hasta que el heap este en orden
        self.sink(1)

        # eliminar el minimo (que esta al final al ser intercambiado)
        return max
    
    def sort(self, a):

        # reemplazamos el heap con el array desordenado que se nos da
        self.heap = [0] + a
        self.n = len(a)

        # ordenamos el heap desde abajo, empezando desde el nivel superior al 
        # ultimo, pues el ultimo no tiene hijos
        for k in range(self.n // 2, 0, -1):
            self.sink(k)

        # iteramos y vamos eliminando el mayor, hasta que el heap este vacio
        while self.n > 1:
            self.exch(1, self.n)
            self.n -= 1

            self.sink(1)

        # devolvemos el heap, que es el arreglo ordenado,
        # lo hacemos desde la posicion 1 porque en nuestra implementacion
        # hacemos los calculos teniendo en cuenta que el heap inicia desde el index 1
        return self.heap[1:]
        

if __name__ == '__main__':

    pq = MinBinaryHeap()

    pq.insert(10)
    pq.insert(15)
    pq.insert(18)
    pq.insert(5)
    pq.insert(8)
    pq.insert(12)

    print("Min heap:")
    print(pq.heap)
    print(pq.delMin())
    print(pq.heap)

    print()
    
    pq2 = MaxBinaryHeap()

    pq2.insert(10)
    pq2.insert(15)
    pq2.insert(18)
    pq2.insert(5)
    pq2.insert(8)
    pq2.insert(12)

    print("Max heap")
    print(pq2.heap)
    print(pq2.delMax())
    print(pq2.heap)

    print("Ordenar: ", [4,5,6,1,2,7,1,45,0])
    print(pq2.sort([4,5,6,1,2,7,1,45,0]))

