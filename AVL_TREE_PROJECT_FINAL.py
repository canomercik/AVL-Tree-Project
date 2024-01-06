
class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if not self.root:  # If the tree is empty, create a new root node
            self.root = AVLNode(key)
        else:
            self.root = self._insert(key, self.root)

    def _insert(self, key, node):
        if key < node.key:
            if node.left is None:  # If the left child is None, create a new node and assign it as the left child
                node.left = AVLNode(key)
            else:
                node.left = self._insert(key, node.left)
        else:
            if node.right is None:  # If the right child is None, create a new node and assign it as the right child
                node.right = AVLNode(key)
            else:
                node.right = self._insert(key, node.right)

        node.height = 1 + max(self.height(node.left), self.height(node.right))  # Update the height of the current node

        return self.balance(node)  # Perform AVL balancing if needed

    def min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def delete(self, key):
        if not self.root:  # If the tree is empty, return False indicating the value was not found
            return False

        self.root, deleted = self._delete(key, self.root)
        return deleted

    def _delete(self, key, node):
        if not node:
            return node, False

        elif key < node.key:
            node.left, deleted = self._delete(key, node.left)
        elif key > node.key:
            node.right, deleted = self._delete(key, node.right)
        else:
            if node.left is None:
                temp = node.right
                node = None
                return temp, True
            elif node.right is None:
                temp = node.left
                node = None
                return temp, True
            temp = self.min_value_node(node.right)  # If the node has both left and right children, find the minimum value node in the right subtree
            node.key = temp.key
            node.right, deleted = self._delete(temp.key, node.right)  # Replace the node's key with the minimum value and delete the minimum value node

        if node is None:
            return node, deleted

        node.height = 1 + max(self.height(node.left), self.height(node.right))   # Update the height of the current node

        return self.balance(node), deleted  # Perform AVL balancing if needed

    def search(self, key):
        return self._search(key, self.root)

    def _search(self, key, node):  # Searchs for required value by checking its left and right nodes
        if not node:
            return False

        elif node.key == key:
            return True

        elif node.key > key:
            return self._search(key, node.left)

        else:
            return self._search(key, node.right)

    def balance_factor(self, node):
        if not node:
            return 0

        return self.height(node.left) - self.height(node.right)

    def height(self, node):
        if not node:
            return 0

        return node.height

    def rotate_left(self, node):
        temp = node.right
        t2 = temp.left

        temp.left = node
        node.right = t2

        node.height = 1 + max(self.height(node.left), self.height(node.right))
        temp.height = 1 + max(self.height(temp.left), self.height(temp.right))

        return temp

    def rotate_right(self, node):
        temp = node.left
        t2 = temp.right

        temp.right = node
        node.left = t2

        node.height = 1 + max(self.height(node.left), self.height(node.right))
        temp.height = 1 + max(self.height(temp.left), self.height(temp.right))

        return temp

    def balance(self, node):
        if not node:
            return node

        if self.balance_factor(node) > 1:
            if self.balance_factor(node.left) < 0:
                node.left = self.rotate_left(node.left)  # Perform a left-right double rotation

            return self.rotate_right(node)

        if self.balance_factor(node) < -1:
            if self.balance_factor(node.right) > 0:
                node.right = self.rotate_right(node.right)  # Perform a right-left double rotation

            return self.rotate_left(node)

        return node

    def traverse(self, node):  # Perform an in-order traversal of the tree and return the list of keys
        result = []
        if node:
            result += self.traverse(node.left)
            result.append(node.key)
            result += self.traverse(node.right)
        return result


if __name__ == '__main__':
    avl_tree = AVLTree()

    while True:
        print("\nAVL Tree Operations")
        print("1. Insert")
        print("2. Delete")
        print("3. Search")
        print("4. Traverse")
        print("5. Quit")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                key = int(input("Enter the value to be inserted: "))
                avl_tree.insert(key)
                print("Value inserted successfully")

            elif choice == 2:
                key = int(input("Enter the value to be deleted: "))
                if avl_tree.delete(key):
                    print("Value deleted successfully")
                else:
                    print("Value not found in the AVL tree")

            elif choice == 3:
                key = int(input("Enter the value to be searched: "))
                if avl_tree.search(key):
                    print("Value found")
                else:
                    print("Value not found")

            elif choice == 4:
                if avl_tree.root is None:
                    print("The AVL tree is empty.")
                else:
                    print("The elements in the AVL tree are:", avl_tree.traverse(avl_tree.root))

            elif choice == 5:
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please enter a valid choice.")

        except ValueError:
            print("Invalid input. Please enter a valid integer choice.")
