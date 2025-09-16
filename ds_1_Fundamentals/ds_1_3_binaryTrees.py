from random import randint

class Node:
    """
    Class-node, instances of the class will be a node of a binary tree

    Attributes:
        value (int): node value
        left (Node): left child node
        right (Node): right child node
    """
    def __init__(self, value: int) -> None:
        """
        Initialize node.
        """
        self.value = value
        self.left = None
        self.right = None

    def __str__(self) -> str:
        """
        String representation of the node.
        """
        return str(self.value)
   
    def __repr__(self) -> str:
        """
        Representation of the node.
        """
        return f"Node({self.value})"


class BinarySearchTree:
    """
    A class for representing the operation of binary trees.

    Attributes:
        root (Node): root of a binary tree.
    """
    def __init__(self) -> None:
        """
        Initialize binary tree.
        """
        self.root = None

    def insert(self, value: int) -> None:
        """
        Insert the value into the tree.
        """
        if not self.root:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node: Node, value: int) -> None:
        """
        Recursively insert value into the tree.
        """
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)
    
    def insert_from_iterable(self, iter_values) -> None:
        """
        Insert a values from iterable object into the tree.
        """
        for iter_value in iter_values:
            self.insert(iter_value)

    def search(self, value: int) -> Node | None:
        """
        Search for a value in the tree.
        
        Returns:
            Node if found, None otherwise
        """
        if self.root is None:
            return None
        return self._search_recursive(self.root, value)
   
    def _search_recursive(self, node: Node | None, value: int) -> Node | None:
        """
        Recursively search for a value.
        """
        if node is None:
            return None
        if value == node.value:
            return node
        elif value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)

    def delete(self, value: int) -> None:
        """
        Delete a value from the tree.
        Does nothing if value not found.
        """
        if not self.search(value):
            return
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node: Node | None, value: int) -> Node | None:
        """
        Recursively delete a value from the tree.
        """
        if node is None:
            return None

        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            if node.left is None and node.right is None:
                return None
            elif node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                max_left_node = self.find_max(node.left)
                node.value = max_left_node.value
                node.left = self._delete_recursive(node.left, max_left_node.value)

        return node

    def find_min(self, node: Node) -> Node:
        """
        Find the minimum value in a subtree.
        """
        if node.left is None:
            return node
        return self.find_min(node.left)

    def find_max(self, node: Node) -> Node:
        """
        Find the maximum value in a subtree.
        """
        if node.right is None:
            return node
        return self.find_max(node.right)

    @property
    def min(self) -> Node | None:
        """
        Get the minimum value in the tree.
        
        Returns:
            Node with minimum value or None if tree is empty
        """
        if self.is_empty():
            return None
        return self.find_min(self.root)
              
    @property
    def max(self) -> Node | None:
        """
        Get the maximum value in the tree.
        
        Returns:
            Node with maximum value or None if tree is empty
        """
        if self.is_empty():
            return None
        return self.find_max(self.root)

    def is_empty(self) -> bool:
        """
        Check if the tree is empty.
        
        Returns:
            True if tree is empty, False otherwise
        """
        return self.root is None
    
    @property
    def height(self) -> int:
        """
        Calculate the height of the tree.
        
        Returns:
            Height of the tree (0 for empty tree)
        """
        return self._height_recursive(self.root)

    def _height_recursive(self, node: Node | None) -> int:
        """
        Recursively calculate height of a subtree.
        """
        if node is None:
            return 0
        return 1 + max(self._height_recursive(node.left), 
                       self._height_recursive(node.right))

    def inorder(self) -> list[int]:
        """
        In-order traversal: Left -> Root -> Right
        Returns values in ascending order.
        
        Returns:
            List of values in in-order sequence
        """
        result: list[int] = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node: Node | None, result: list[int]) -> None:
        """
        Recursively perform in-order traversal.
        """
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

    def preorder(self) -> list[int]:
        """
        Pre-order traversal: Root -> Left -> Right
        Useful for copying tree structure.
        
        Returns:
            List of values in pre-order sequence
        """
        result: list[int] = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node: Node | None, result: list[int]) -> None:
        """
        Recursively perform pre-order traversal.
        """
        if node:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    def postorder(self) -> list[int]:
        """
        Post-order traversal: Left -> Right -> Root
        Useful for deleting tree nodes.
        
        Returns:
            List of values in post-order sequence
        """
        result: list[int] = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, node: Node | None, result: list[int]) -> None:
        """
        Recursively perform post-order traversal.
        """
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)

    def clear(self) -> None:
        """
        Clear the entire tree.
        Uses post-order traversal for proper memory management.
        """
        self.root = None

    def _build_tree_string(self, node: Node | None, prefix: str, is_left: bool) -> str:
        """
        Visual tree representation.

        Args:
            node: Current node to process
            prefix: Prefix string for formatting
            is_left: Whether the node is a left child

        Returns:
            String representation of the tree
        """
        result = ""

        if node is None:
            return result

        result += self._build_tree_string(node.right, prefix + ("│   " if is_left else "    "), False)
        result += prefix + ("└── " if is_left else "┌── ") + str(node.value) + "\n"
        result += self._build_tree_string(node.left, prefix + ("    " if is_left else "│   "), True)

        return result

    def __contains__(self, value) -> bool:
        """
        Search the value in the tree.

        Returns:
            True if value in the tree, False otherwise
        """
        if self.search(value) is not None:
            return True
        return False

    def __str__(self) -> str:
        """
        String representation of the tree.
        
        Returns:
            Visual representation of the tree or 'Empty tree'
        """
        if self.is_empty():
            return "Empty tree"
        return self._build_tree_string(self.root, "", True)

