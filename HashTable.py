def bernstein_hash(key):
    hash_value = 0
    for char in key:
        hash_value = 33 * hash_value + ord(char)

    return hash_value

def djb2_hash(key):
    hash_value = 5381
    for char in key:
        hash_value = (hash_value * 33) ^ ord(char)
    
    return hash_value

class Hast_table_sc:

    def __init__(self, size = 7):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def djb2_hash(self, key):
        hash_value = 5381
        for char in key:
            hash_value = (hash_value * 33) ^ ord(char)

        return hash_value % self.size
    
    def bernstein_hash(self, key):
        hash_value = 0
        for char in key:
            hash_value = 33 * hash_value + ord(char)

        return hash_value % self.size

    def set_item(self, key, value):
        index = self.djb2_hash(key)

        bucket = self.table[index]

        for e in bucket: 
            if e[0] == key:
                e[1] = value
                return 
            
        bucket.append([key, value])

    def get_item(self, key):
        index = self.djb2_hash(key)
        bucket = self.table[index]

        for e in bucket:
            if e[0] == key:
                return e[1]
            
        return None

    def remove_item(self, key):
        index = self.djb2_hash(key)
        bucket = self.table[index]

        for i in range(len(bucket)):
            if bucket[i][0] == key:
                return bucket.pop(i)
            
        return None
    
    def keys(self):

        keys = []

        for i in range(self.size):
            for e in self.table[i]:
                keys.append(e[0])

        return keys
    
    def values(self):

        values = []

        for i in range(self.size):
            for e in self.table[i]:
                values.append(e[1])

        return values
    
    def items(self):

        items = []

        for i in range(self.size):
            for e in self.table[i]:
                items.append(e)

        return items