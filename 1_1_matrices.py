import itertools
from typing import List, Union


class Matrix2D:
    """
    A class to represent a 2D mathematical matrix and perform basic linear algebra operations.
    
    Attributes:
        matrix (List[List[Union[int, float]]]): The 2D list representing the matrix
        rows (int): Number of rows in the matrix
        cols (int): Number of columns in the matrix
    """
    
    def __init__(self, matrix: List[List[Union[int, float]]]) -> None:
        """
        Initialize Matrix2D with a 2D list.
        
        Args:
            matrix: 2D list of integers or floats representing the matrix
            
        Raises:
            ValueError: If matrix is empty, not 2D, or has inconsistent row lengths
        """
        self.matrix = self._validate_matrix(matrix)
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0]) if self.rows > 0 else 0

    @staticmethod
    def _validate_matrix(matrix: List[List]) -> List[List[Union[int, float]]]:
        """
        Validate that the input is a proper 2D matrix.
        
        Args:
            matrix: Input to validate
            
        Returns:
            Validated 2D matrix
            
        Raises:
            ValueError: If matrix is invalid
        """
        if not matrix or not isinstance(matrix, list):
            raise ValueError("Matrix must be a non-empty list.")

        row_length = len(matrix[0])
        for i, row in enumerate(matrix):
            if not isinstance(row, list):
                raise ValueError(f"Row {i} is not a list.")
            if len(row) != row_length:
                raise ValueError("All rows must be of the same length.")
            for j, element in enumerate(row):
                if not isinstance(element, (int, float)):
                    raise ValueError(f"Element at position ({i},{j}) is not a number.")
        
        return matrix

    @staticmethod
    def det_2x2(matrix: List[List[Union[int, float]]]) -> Union[int, float]:
        """
        Calculate determinant of a 2x2 matrix.
        
        Args:
            matrix: 2x2 matrix as list of lists
            
        Returns:
            Determinant value
        """
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    def det(self) -> Union[int, float]:
        """
        Calculate determinant using recursive expansion by minors.
        
        Returns:
            Determinant value
            
        Raises:
            ValueError: If matrix is not square
        """
        if self.rows != self.cols:
            raise ValueError("Matrix must be square to calculate determinant.")
        
        if self.rows == 1:
            return self.matrix[0][0]
        
        if self.rows == 2:
            return self.det_2x2(self.matrix)
        
        determinant = 0
        for j in range(self.cols):
            minor_matrix = []
            for i in range(1, self.rows):
                row = []
                for k in range(self.cols):
                    if k != j:
                        row.append(self.matrix[i][k])
                minor_matrix.append(row)
            
            minor = Matrix2D(minor_matrix)
            sign = 1 if j % 2 == 0 else -1
            determinant += sign * self.matrix[0][j] * minor.det()
        
        return determinant

    def det_permutations(self) -> Union[int, float]:
        """
        Calculate determinant using permutation formula (Leibniz formula).
        Warning: O(n!) complexity, only for small matrices.
        
        Returns:
            Determinant value
            
        Raises:
            ValueError: If matrix is not square
        """
        if self.rows != self.cols:
            raise ValueError("Matrix must be square to calculate determinant.")
        
        n = self.rows
        if n == 1:
            return self.matrix[0][0]
        elif n == 2:
            return self.det_2x2(self.matrix)
        
        determinant = 0
        for perm in itertools.permutations(range(n)):
            # Calculate sign of permutation
            sign = 1
            for i in range(n):
                for j in range(i + 1, n):
                    if perm[i] > perm[j]:
                        sign *= -1
            
            # Calculate product of diagonal elements
            product = 1
            for i in range(n):
                product *= self.matrix[i][perm[i]]
            
            determinant += sign * product
        
        return determinant

    def transpose(self) -> 'Matrix2D':
        """
        Return the transpose of the matrix.
        
        Returns:
            New Matrix2D instance that is the transpose
        """
        transposed = []
        for j in range(self.cols):
            new_row = []
            for i in range(self.rows):
                new_row.append(self.matrix[i][j])
            transposed.append(new_row)
        
        return Matrix2D(transposed)

    @property
    def T(self) -> 'Matrix2D':
        """Property access to transpose (NumPy-style)."""
        return self.transpose()

    def __add__(self, other: 'Matrix2D') -> 'Matrix2D':
        """
        Add two matrices of the same dimensions.
        
        Args:
            other: Another Matrix2D instance
            
        Returns:
            New Matrix2D instance with sum
            
        Raises:
            TypeError: If other is not Matrix2D
            ValueError: If matrices have different dimensions
        """
        if not isinstance(other, Matrix2D):
            raise TypeError("Can only add another Matrix2D instance.")
        
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have same dimensions for addition.")
        
        result = [
            [self.matrix[i][j] + other.matrix[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        
        return Matrix2D(result)

    def __sub__(self, other: 'Matrix2D') -> 'Matrix2D':
        """
        Subtract two matrices of the same dimensions.
        
        Args:
            other: Another Matrix2D instance
            
        Returns:
            New Matrix2D instance with difference
            
        Raises:
            TypeError: If other is not Matrix2D
            ValueError: If matrices have different dimensions
        """
        if not isinstance(other, Matrix2D):
            raise TypeError("Can only subtract another Matrix2D instance.")
        
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have same dimensions for subtraction.")
        
        result = [
            [self.matrix[i][j] - other.matrix[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        
        return Matrix2D(result)

    def __mul__(self, scalar: Union[int, float]) -> 'Matrix2D':
        """
        Multiply matrix by a scalar.
        
        Args:
            scalar: Number to multiply by
            
        Returns:
            New Matrix2D instance with scaled values
            
        Raises:
            TypeError: If scalar is not int or float
        """
        if not isinstance(scalar, (int, float)):
            raise TypeError("Can only multiply by scalar (int or float).")
        
        result = [
            [self.matrix[i][j] * scalar for j in range(self.cols)]
            for i in range(self.rows)
        ]
        
        return Matrix2D(result)

    def __rmul__(self, scalar: Union[int, float]) -> 'Matrix2D':
        """
        Right multiplication by scalar (for scalar * matrix).
        """
        return self.__mul__(scalar)

    def __matmul__(self, other: 'Matrix2D') -> 'Matrix2D':
        """
        Matrix multiplication.
        
        Args:
            other: Another Matrix2D instance
            
        Returns:
            New Matrix2D instance with product
            
        Raises:
            TypeError: If other is not Matrix2D
            ValueError: If dimensions are incompatible
        """
        if not isinstance(other, Matrix2D):
            raise TypeError("Can only multiply with another Matrix2D instance.")
        
        if self.cols != other.rows:
            raise ValueError(
                "Number of columns in first matrix must equal "
                "number of rows in second matrix for multiplication."
            )
        
        result = []
        for i in range(self.rows):
            row = []
            for j in range(other.cols):
                element = 0
                for k in range(self.cols):
                    element += self.matrix[i][k] * other.matrix[k][j]
                row.append(element)
            result.append(row)
        
        return Matrix2D(result)

    def __eq__(self, other: object) -> bool:
        """
        Check equality with another matrix.
        
        Args:
            other: Object to compare with
            
        Returns:
            True if matrices are equal, False otherwise
        """
        if not isinstance(other, Matrix2D):
            return False
        return self.matrix == other.matrix

    def __str__(self) -> str:
        """String representation of the matrix."""
        return str(self.matrix)

    def __repr__(self) -> str:
        """Representation of the matrix."""
        return f"Matrix2D({self.matrix})"
      
