class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    
    def __init__(self):
        self.root = None


    def height(self, node):
        if not node:
            return 0
        
        return node.height

    def get_balance(self, node):
        return self.height(node.left) - self.height(node.right)
    
    def rotate_right(self, node):
        x: Node = node.left
        node.left = x.right
        x.right = node

        node.height = 1 + max(self.height(node.left), self.height(node.right))
        x.height = 1 + max(self.height(x.left), self.height(x.right))

        return x
    
    def rotate_left(self, node):
        x: Node = node.right
        node.right = node.left
        x.left = node

        node.height = 1 + max(self.height(node.left), self.height(node.right))
        x.height = 1 + max(self.height(x.left), self.height(x.right))

        return x


    def insert(self, value):
        self.root = self.insert_helper(self.root, value)

    def insert_helper(self, node, value):
        
        if not node:
            return Node(value)
        
        if value < node.value:
            node.left = self.insert_helper(node.left, value)
        elif value > node.value:
            node.right = self.insert_helper(node.right, value)
        else:
            return node
        
        node.height = 1 + max(self.height(node.left), self.height(node.right))

        balance = self.get_balance(node)
        if balance > 1 and value < node.left.value:
            node = self.rotate_right(node)

        if balance < -1 and value > node.right.value:
            node = self.rotate_left(node)

        if balance > 1 and value > node.left.value:
            node.left = self.rotate_left(node)
            node = self.rotate_right(node)

        if balance < -1 and value < node.right.value:
            node.right = self.rotate_right(node.right)
            node = self.rotate_left(node)

        return node


    def min(self, node):
        x = node

        while x.left:
            x = x.left

        return x


    def delete(self, value):
        self.root = self.delete_helper(self.root, value)

    def delete_min(self, node):

        if not node.left:
            return node.right
        node.left = self.delete_min(node.left)
        node.height = 1 + max(self.height(node.left), self.height(node.right))

        return node

    def delete_helper(self, node, value):

        if not node:
            return None
        
        if value < node.value:
            node.left = self.delete(node.left, value)
        elif value  > node.value:
            node.right = self.delete(node.right, value)
        else:
            
            # handles case 0 and case 1; only 1 child or no childs
            if not node.right:
                return node.left
            if not node.left:
                return node.right
        

            # handles case 2: do the change of references to the links
            t: Node = node

            # find the smallest node in the right subtree
            node = self.min(t.right)

            # set the right link, to a subtree where the smallest value is deleted
            node.right = self.delete_min(t.right)

            # set the left link to the original left link of the node to be deleted
            node.left = t.left

        if not node:
            return None

        node.height = 1 + max(self.height(node.left), self.height(node.right))

        balance = self.get_balance(node)
        if balance > 1 and self.get_balance(node.left) >= 0:
            node = self.rotate_right(node)

        if balance < -1 and self.get_balance(node.right) <= 0:
            node = self.rotate_left(node)

        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.rotate_left(node.left)
            node = self.rotate_right(node)

        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.rotate_right(node.right)
            node = self.rotate_left(node)

        return node 
    
    def get(self, value) -> Node:
        aux: Node = self.root
        
        while(aux != None):
            if aux.value < value:
                aux = aux.right
            elif aux.value > value:
                aux = aux.left
            else:
                return aux
        
        return None


if __name__ == "__main__":

    tree = AVLTree()

    tree.insert(1)
    tree.insert(2)
    tree.insert(3)
    tree.insert(4)
    tree.insert(5)
    tree.insert(6)
    tree.insert(7)

    print(tree.root.value)
    print(tree.root.left.value)
    print(tree.root.left.left.value)
    print(tree.root.right.value)

    tree.delete(4)
    print()

    print(tree.root.value)
    print(tree.root.left.value)
    print(tree.root.left.left.value)
    print(tree.root.right.value)