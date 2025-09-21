import pytest
from ds_1_3_binaryTrees import BinarySearchTree, Node 


class TestBST:
    """
    Класс тестирования бинарного дерева поиска.
    """

    def test_insert_and_in_value(self):
        """
        Вставка значений и поиск в дереве.
        """
        bst = BinarySearchTree()

        bst.insert(1)
        bst.insert(3)
        bst.insert(2)
        bst.insert(5)

        assert 2 in bst
        assert (4 in bst) == False
        
    def test_insert_from_iterable(self):
        """
        Вставка значений в дерево из итерируемого объекта.
        """
        # Тест 1
        bst = BinarySearchTree()
        values_list = [1,3,57,4,7,9,2,5,6,2,34,45,6]

        bst.insert_from_iterable(values_list)

        for value in values_list:
            assert value in bst

        assert 11 not in bst

        #Тест 2
        bst1 = BinarySearchTree()
        values_list = (1,3,57,4,7,9,2,5,6,2,34,45,6)

        bst1.insert_from_iterable(values_list)

        for value in values_list:
            assert value in bst1

        assert 11 not in bst1

    def test_search_value(self):
        """
        Тест поиска значений через search.
        """
        bst = BinarySearchTree()

        bst.insert(1)
        bst.insert(2)

        assert bst.search(2).value == 2
        assert bst.search(3) == None
    
    def test_delete_value(self):
        """
        Тест удаления значений.
        """
        bst = BinarySearchTree()
        values = [1,3,7,8,4,2,7,8]

        bst.insert_from_iterable(values)
        
        bst.delete(8)
        assert 8 in bst

        bst.delete(8)
        assert 8 not in bst

    def test_min_and_max(self):
        """
        Тест нахождения максимального и минимального значений.
        """
        bst = BinarySearchTree()
        values = [-1,5,7,8,23,-3,1,-9]

        bst.insert_from_iterable(values)

        assert bst.min.value == -9
        assert bst.max.value == 23
    
    def test_is_empty(self):
        """
        Тест метода is_empty.
        """
        bst = BinarySearchTree()

        assert bst.is_empty()

    def test_height(self):
        """
        Тест определения высоты дерева.
        """
        bst = BinarySearchTree()
        values = set(range(10))

        bst.insert_from_iterable(values)

        assert bst.height == 10

        bst.delete(3)
        assert bst.height == 9

    def test_traversals(self):
        """
        Тест трех видов обходов дерева.
        """
        bst = BinarySearchTree()
        values = (7,5,8,4,6,9,3)
        
        bst.insert_from_iterable(values)

        assert bst.inorder() == [3,4,5,6,7,8,9]
        assert bst.preorder() == [7,5,4,3,6,8,9]
        assert bst.postorder() == [3,4,6,5,9,8,7]
    
    def test_clear(self):
        """
        Тест очистки дерева
        """
        bst = BinarySearchTree()
        values = set(range(10))

        bst.insert_from_iterable(values)
        assert 1 in bst

        bst.clear()
        assert 1 not in bst
        assert bst.is_empty()
        
    def test_empty_tree_operations(self):
        """
        Тест операций на пустом дереве
        """
        bst = BinarySearchTree()
        assert bst.is_empty()
        assert bst.height == 0
        assert bst.inorder() == []
        assert bst.preorder() == []
        assert bst.postorder() == []
        assert bst.min is None
        assert bst.max is None
        assert bst.search(1) is None

