import pytest
from ds_1_1_matrices import Matrix2D


class TestMatrix2D:
    """Тесты для класса Matrix2D"""

    def test_valid_matrix_creation(self):
        """Тест создания корректной матрицы"""
        matrix_data = [[1, 2], [3, 4]]
        matrix = Matrix2D(matrix_data)
        assert matrix.matrix == matrix_data
        assert matrix.rows == 2
        assert matrix.cols == 2

    def test_invalid_matrix_empty(self):
        """Тест создания пустой матрицы"""
        with pytest.raises(ValueError, match="Matrix must be a non-empty list"):
            Matrix2D([])

    def test_invalid_matrix_not_list(self):
        """Тест создания матрицы не из списка"""
        with pytest.raises(ValueError, match="Matrix must be a non-empty list"):
            Matrix2D("not a list")

    def test_invalid_matrix_ragged_rows(self):
        """Тест создания матрицы с разной длиной строк"""
        with pytest.raises(ValueError, match="All rows must be of the same length"):
            Matrix2D([[1, 2], [3, 4, 5]])

    def test_invalid_matrix_non_numeric(self):
        """Тест создания матрицы с нечисловыми элементами"""
        with pytest.raises(ValueError, match="is not a number"):
            Matrix2D([[1, 2], ["a", 4]])

    def test_1x1_matrix(self):
        """Тест матрицы 1x1"""
        matrix = Matrix2D([[5]])
        assert matrix.rows == 1
        assert matrix.cols == 1
        assert matrix.det() == 5

    def test_2x2_det(self):
        """Тест определителя 2x2 матрицы"""
        matrix = Matrix2D([[1, 2], [3, 4]])
        assert matrix.det() == -2
        assert matrix.det_2x2(matrix.matrix) == -2

    def test_3x3_det(self):
        """Тест определителя 3x3 матрицы"""
        matrix = Matrix2D([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        assert matrix.det() == 0  # Вырожденная матрица

    def test_det_non_square(self):
        """Тест определителя неквадратной матрицы"""
        matrix = Matrix2D([[1, 2, 3], [4, 5, 6]])
        with pytest.raises(ValueError, match="Matrix must be square"):
            matrix.det()

    def test_det_permutations_vs_recursive(self):
        """Сравнение двух методов вычисления определителя"""
        test_matrices = [
            [[2, 1], [3, 4]],
            [[1, 2, 3], [0, 1, 4], [5, 6, 0]],
            [[4, 3], [2, 1]]
        ]
        
        for matrix_data in test_matrices:
            matrix = Matrix2D(matrix_data)
            det_recursive = matrix.det()
            det_permutations = matrix.det_permutations()
            assert abs(det_recursive - det_permutations) < 1e-10

    def test_transpose(self):
        """Тест транспонирования"""
        matrix = Matrix2D([[1, 2, 3], [4, 5, 6]])
        transposed = matrix.transpose()
        expected = [[1, 4], [2, 5], [3, 6]]
        assert transposed.matrix == expected

    def test_T_property(self):
        """Тест свойства T"""
        matrix = Matrix2D([[1, 2], [3, 4]])
        assert matrix.T.matrix == [[1, 3], [2, 4]]

    def test_matrix_addition(self):
        """Тест сложения матриц"""
        matrix1 = Matrix2D([[1, 2], [3, 4]])
        matrix2 = Matrix2D([[5, 6], [7, 8]])
        result = matrix1 + matrix2
        expected = [[6, 8], [10, 12]]
        assert result.matrix == expected

    def test_matrix_addition_different_dimensions(self):
        """Тест сложения матриц разной размерности"""
        matrix1 = Matrix2D([[1, 2]])
        matrix2 = Matrix2D([[3, 4, 5]])
        with pytest.raises(ValueError, match="same dimensions for addition"):
            matrix1 + matrix2

    def test_matrix_subtraction(self):
        """Тест вычитания матриц"""
        matrix1 = Matrix2D([[5, 6], [7, 8]])
        matrix2 = Matrix2D([[1, 2], [3, 4]])
        result = matrix1 - matrix2
        expected = [[4, 4], [4, 4]]
        assert result.matrix == expected

    def test_scalar_multiplication(self):
        """Тест умножения на скаляр"""
        matrix = Matrix2D([[1, 2], [3, 4]])
        result = matrix * 3
        expected = [[3, 6], [9, 12]]
        assert result.matrix == expected

    def test_scalar_multiplication_right(self):
        """Тест правого умножения на скаляр"""
        matrix = Matrix2D([[1, 2], [3, 4]])
        result = 3 * matrix
        expected = [[3, 6], [9, 12]]
        assert result.matrix == expected

    def test_matrix_multiplication(self):
        """Тест умножения матриц"""
        matrix1 = Matrix2D([[1, 2], [3, 4]])
        matrix2 = Matrix2D([[5, 6], [7, 8]])
        result = matrix1 @ matrix2
        expected = [[19, 22], [43, 50]]
        assert result.matrix == expected

    def test_matrix_multiplication_incompatible(self):
        """Тест умножения несовместимых матриц"""
        matrix1 = Matrix2D([[1, 2, 3]])
        matrix2 = Matrix2D([[4], [5]])
        with pytest.raises(ValueError, match="Number of columns in first matrix"):
            matrix1 @ matrix2

    def test_equality(self):
        """Тест сравнения матриц"""
        matrix1 = Matrix2D([[1, 2], [3, 4]])
        matrix2 = Matrix2D([[1, 2], [3, 4]])
        matrix3 = Matrix2D([[5, 6], [7, 8]])
        
        assert matrix1 == matrix2
        assert matrix1 != matrix3
        assert matrix1 != "not a matrix"

    def test_string_representation(self):
        """Тест строкового представления"""
        matrix = Matrix2D([[1, 2], [3, 4]])
        assert str(matrix) == "[[1, 2], [3, 4]]"
        assert repr(matrix) == "Matrix2D([[1, 2], [3, 4]])"

    def test_complex_matrix_operations(self):
        """Тест комплексных операций с матрицами"""
        # Создаем тестовые матрицы
        A = Matrix2D([[1, 2], [3, 4]])
        B = Matrix2D([[5, 6], [7, 8]])
        C = Matrix2D([[9, 10], [11, 12]])
        
        # Проверяем ассоциативность: (A + B) + C = A + (B + C)
        result1 = (A + B) + C
        result2 = A + (B + C)
        assert result1 == result2
        
        # Проверяем дистрибутивность: A @ (B + C) = A@B + A@C
        result3 = A @ (B + C)
        result4 = (A @ B) + (A @ C)
        assert result3 == result4

    def test_determinant_properties(self):
        """Тест свойств определителя"""
        # det(A@B) = det(A) * det(B)
        A = Matrix2D([[2, 1], [1, 3]])
        B = Matrix2D([[4, 2], [1, 5]])
        
        det_A = A.det()
        det_B = B.det()
        det_AB = (A @ B).det()
        
        assert abs(det_AB - (det_A * det_B)) < 1e-10
        
        # det(A^T) = det(A)
        assert abs(A.det() - A.T.det()) < 1e-10

    def test_edge_cases(self):
        """Тест крайних случаев"""
        # Нулевая матрица
        zero_matrix = Matrix2D([[0, 0], [0, 0]])
        assert zero_matrix.det() == 0
        
        # Единичная матрица
        identity_like = Matrix2D([[1, 0], [0, 1]])
        assert identity_like.det() == 1
        
        # Матрица с отрицательными числами
        negative_matrix = Matrix2D([[-1, -2], [-3, -4]])
        assert negative_matrix.det() == -2

