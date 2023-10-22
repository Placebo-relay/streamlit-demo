import streamlit as st
import numpy as np

def main():
    st.title("Matrix Operations")

    print("______\n")
    print("\n p2: [9] => T6: matrix operations on 2x[M]x[N] of double\n")
    print("______")

    rows1 = st.number_input("number of rows for the first matrix", min_value=1, value=1)
    cols1 = st.number_input("number of columns for the first matrix", min_value=1, value=1)

    rows2 = st.number_input("number of rows for the second matrix", min_value=1, value=1)
    cols2 = st.number_input("number of columns for the second matrix", min_value=1, value=1)

    matrix1 = np.random.randn(rows1, cols1) * 100.0
    matrix2 = np.random.randn(rows2, cols2) * 100.0

    rank1 = np.linalg.matrix_rank(matrix1)
    rank2 = np.linalg.matrix_rank(matrix2)
    transpose1 = matrix1.T
    transpose2 = matrix2.T
    square1 = (rows1 == cols1)
    square2 = (rows2 == cols2)
    determinant1, determinant2 = 0.0, 0.0
    trace1, trace2 = 0.0, 0.0
    inverse1, inverse2 = None, None
    invertible1, invertible2 = False, False

    if square1:
        determinant1 = np.linalg.det(matrix1)
        trace1 = np.trace(matrix1)
        if determinant1 != 0:
            inverse1 = np.linalg.inv(matrix1)
            invertible1 = True

    if square2:
        determinant2 = np.linalg.det(matrix2)
        trace2 = np.trace(matrix2)
        if determinant2 != 0:
            inverse2 = np.linalg.inv(matrix2)
            invertible2 = True

    sum_matrix, product = None, None
    addable = (matrix1.shape == matrix2.shape)
    equal = (addable and np.array_equal(matrix1, matrix2))
    multipliable = (matrix1.shape[1] == matrix2.shape[0])

    if addable:
        sum_matrix = matrix1 + matrix2

    if multipliable:
        product = np.dot(matrix1, matrix2)

    st.subheader("Matrix 1")
    st.write(matrix1)

    st.subheader("Matrix 2")
    st.write(matrix2)

    st.subheader("Rank")
    st.write("Matrix 1:", rank1)
    st.write("Matrix 2:", rank2)

    st.subheader("Transpose")
    st.write("Matrix 1:")
    st.write(transpose1)
    st.write("Matrix 2:")
    st.write(transpose2)

    if square1:
        st.subheader("Matrix 1 (square) Properties")
        st.write("Determinant:", determinant1)
        st.write("Trace:", trace1)
        if invertible1:
            st.write("Inverse:")
            st.write(inverse1)
        else:
            st.write("Matrix 1 is not invertible.")
    else:
        st.subheader("Matrix 1 is not square.")

    if square2:
        st.subheader("Matrix 2 (square) Properties")
        st.write("Determinant:", determinant2)
        st.write("Trace:", trace2)
        if invertible2:
            st.write("Inverse:")
            st.write(inverse2)
        else:
            st.write("Matrix 2 is not invertible.")
    else:
        st.subheader("Matrix 2 is not square.")

    st.subheader("Combo Operations")
    st.write("Are the matrices equal?", "Yes" if equal else "No")

    if addable:
        st.write("Sum of Matrix 1 and Matrix 2:")
        st.write(sum_matrix)
    else:
        st.write("Matrices cannot be added.")

    if multipliable:
        st.write("Product of Matrix 1 and Matrix 2:")
        st.write(product)
    else:
        st.write("Matrices cannot be multiplied.")

if __name__ == "__main__":
    main()
