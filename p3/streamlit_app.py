import streamlit as st
from streamlit import file_uploader
import random

def display_file_contents():
    with open('random_file.txt', 'r') as file:
        contents = file.read()
    st.text_area("File Contents", value=contents, height=200)

def main():
    st.title("File Relocator")

    # Create a sidebar with options to generate or upload a file
    st.sidebar.title("Options")
    option = st.sidebar.radio("Select an option:", ("Generate Random File", "Upload File"))

    if option == "Generate Random File":
        num_lines = st.sidebar.slider("Number of Lines", 5, 10, 5)
        generate_random_file(num_lines)
        st.success(f"Generated random file with {num_lines} lines.")

    elif option == "Upload File":
        uploaded_file = st.sidebar.file_uploader("Upload a file")
        if uploaded_file is not None:
            file_contents = uploaded_file.read()
            with open('random_file.txt', 'wb') as file:
                file.write(file_contents)
            st.success("Uploaded file successfully.")

    # Display file contents
    display_file_contents()

    # Create widgets for inputting line numbers
    num_lines = sum(1 for line in open('random_file.txt'))
    n = st.number_input("Line n:", min_value=1, max_value=num_lines, value=1, step=1)
    m = st.number_input("Line m:", min_value=1, max_value=num_lines, value=1, step=1)

    # Button to relocate lines
    if st.button("Relocate"):
        if n == m:
            st.error("Error: Line n and Line m must have different values.")
        elif n - 1 == m:
            st.error("Error: Line n is already after Line m.")
        else:
            relocate_line(n, m)
            st.success(f"Line {n} relocated after Line {m}.")

if __name__ == "__main__":
    main()
