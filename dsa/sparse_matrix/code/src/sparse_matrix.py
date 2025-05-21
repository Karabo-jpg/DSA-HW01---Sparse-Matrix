# sparse_matrix.py
# Author: Karabo Ojiambo
# Date: May 21, 2025
# Description: Implementation of a Sparse Matrix class for DSA-HW01 assignment.
# This code reads sparse matrices from files, performs addition, subtraction, and multiplication,
# and handles input variations as per assignment requirements. No external libraries beyond
# standard Python are used, adhering to the constraint of custom implementation.

class SparseMatrix:
    def __init__(self, matrix_file_path=None, num_rows=None, num_cols=None):
        """Initialize SparseMatrix either by loading from a file or creating an empty matrix.
        
        Args:
            matrix_file_path (str, optional): Path to the input file.
            num_rows (int, optional): Number of rows for an empty matrix.
            num_cols (int, optional): Number of columns for an empty matrix.
        
        Raises:
            ValueError: If file cannot be opened or format is invalid.
        """
        self.elements = []  # List of tuples (row, col, value) for non-zero elements
        if matrix_file_path:
            self._load_from_file(matrix_file_path)
        elif num_rows is not None and num_cols is not None:
            self.rows = num_rows
            self.cols = num_cols
        else:
            raise ValueError("Must provide either file path or dimensions")

    def _load_from_file(self, matrix_file_path):
        """Load sparse matrix data from a file with custom parsing.
        
        The file format is: rows=<num>, cols=<num>, followed by (row,col,value) entries.
        Ignores whitespace and throws ValueError for invalid formats.
        """
        matrix_file_path = matrix_file_path.strip()  # Ensure no leading/trailing spaces
        try:
            with open(matrix_file_path, 'r') as file:
                lines = [line.strip() for line in file if line.strip()]  # Remove empty lines and whitespace
                if len(lines) < 2:
                    raise ValueError("Input file has wrong format")

                # Parse rows and cols
                if not lines[0].startswith("rows=") or not lines[1].startswith("cols="):
                    raise ValueError("Input file has wrong format")
                self.rows = int(lines[0][5:])
                self.cols = int(lines[1][5:])

                # Parse non-zero elements
                for line in lines[2:]:
                    if not line or line[0] != '(' or line[-1] != ')':
                        raise ValueError("Input file has wrong format")
                    content = line[1:-1].split(',')
                    if len(content) != 3:
                        raise ValueError("Input file has wrong format")
                    try:
                        row, col, value = map(int, content)
                        if not (0 <= row < self.rows and 0 <= col < self.cols):
                            raise ValueError("Invalid row or column index")
                        self.elements.append((row, col, value))
                    except ValueError:
                        raise ValueError("Input file has wrong format")
        except FileNotFoundError:
            raise ValueError("Cannot open file")

    def get_element(self, curr_row, curr_col):
        """Retrieve the value at the specified position, returning 0 for non-zero elements.
        
        Args:
            curr_row (int): Row index.
            curr_col (int): Column index.
        
        Raises:
            ValueError: If indices are out of bounds.
        """
        if not (0 <= curr_row < self.rows and 0 <= curr_col < self.cols):
            raise ValueError("Invalid row or column")
        for row, col, value in self.elements:
            if row == curr_row and col == curr_col:
                return value
        return 0

    def set_element(self, curr_row, curr_col, value):
        """Set the value at the specified position, removing if value is 0.
        
        Args:
            curr_row (int): Row index.
            curr_col (int): Column index.
            value (int): Value to set.
        
        Raises:
            ValueError: If indices are out of bounds.
        """
        if not (0 <= curr_row < self.rows and 0 <= curr_col < self.cols):
            raise ValueError("Invalid row or column")
        for i, (row, col, _) in enumerate(self.elements):
            if row == curr_row and col == curr_col:
                if value == 0:
                    self.elements.pop(i)
                else:
                    self.elements[i] = (row, col, value)
                return
        if value != 0:
            self.elements.append((curr_row, curr_col, value))

    def add(self, other):
        """Add two sparse matrices.
        
        Args:
            other (SparseMatrix): Another sparse matrix.
        
        Raises:
            ValueError: If dimensions do not match.
        
        Returns:
            SparseMatrix: Result of addition.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions do not match for addition")
        result = SparseMatrix(self.rows, self.cols)
        # Copy elements from self
        for row, col, value in self.elements:
            result.set_element(row, col, value)
        # Add elements from other
        for row, col, value in other.elements:
            current_val = result.get_element(row, col)
            result.set_element(row, col, current_val + value)
        return result

    def subtract(self, other):
        """Subtract two sparse matrices.
        
        Args:
            other (SparseMatrix): Another sparse matrix.
        
        Raises:
            ValueError: If dimensions do not match.
        
        Returns:
            SparseMatrix: Result of subtraction.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions do not match for subtraction")
        result = SparseMatrix(self.rows, self.cols)
        for row, col, value in self.elements:
            result.set_element(row, col, value)
        for row, col, value in other.elements:
            current_val = result.get_element(row, col)
            result.set_element(row, col, current_val - value)
        return result

    def multiply(self, other):
        """Multiply two sparse matrices.
        
        Args:
            other (SparseMatrix): Another sparse matrix.
        
        Raises:
            ValueError: If dimensions do not match (cols of self != rows of other).
        
        Returns:
            SparseMatrix: Result of multiplication.
        """
        if self.cols != other.rows:
            raise ValueError("Matrix dimensions do not match for multiplication")
        result = SparseMatrix(self.rows, other.cols)
        for i1, j1, v1 in self.elements:
            for i2, j2, v2 in other.elements:
                if j1 == i2:  # Matching columns and rows for multiplication
                    current_val = result.get_element(i1, j2)
                    result.set_element(i1, j2, current_val + (v1 * v2))
        return result

    def save_to_file(self, output_file_path):
        """Save the sparse matrix to a file in the specified format.
        
        Args:
            output_file_path (str): Path to the output file.
        """
        output_file_path = output_file_path.strip()  # Ensure no spaces in output path
        with open(output_file_path, 'w') as file:
            file.write(f"rows={self.rows}\n")
            file.write(f"cols={self.cols}\n")
            for row, col, value in self.elements:
                file.write(f"({row}, {col}, {value})\n")

def main():
    """Main function to handle user interaction and matrix operations."""
    try:
        file1 = input("Enter path to first matrix file: ").strip()
        file2 = input("Enter path to second matrix file: ").strip()

        matrix1 = SparseMatrix(file1)
        matrix2 = SparseMatrix(file2)

        print("Select operation:\n1. Addition\n2. Subtraction\n3. Multiplication")
        choice = int(input("Enter choice (1-3): "))
        # Clear the input buffer to prevent Bad File Descriptor error
        input()  # Consume the leftover newline

        result = None
        if choice == 1:
            result = matrix1.add(matrix2)
        elif choice == 2:
            result = matrix1.subtract(matrix2)
        elif choice == 3:
            result = matrix1.multiply(matrix2)
        else:
            raise ValueError("Invalid operation choice")

        output_file = input("Enter output file path: ").strip()
        result.save_to_file(output_file)
        print(f"Operation completed. Result saved to {output_file}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
