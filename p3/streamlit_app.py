import streamlit as st
from streamlit import file_uploader
import random

def generate_random_file(num_lines):
    with open('random_file.txt', 'w') as file:
        for i in range(num_lines):
            file.write(f'Line {i+1}\n')

def relocate_line(n, m):
    with open('random_file.txt', 'r') as file:
        lines = file.readlines()

    line_n = lines.pop(n-1)
    lines.insert(m, line_n)

    with open('random_file.txt', 'w') as file:
        file.writelines(lines)

def display_file_contents():
    with open('random_file.txt', 'r') as file:
        contents = file.read()
    st.text_area("File Contents", value=contents, height=200)
    
def display_modified_file_contents():
    with open('random_file_modified.txt', 'r') as file:
        contents = file.read()
    st.text_area("Modified File Contents", value=contents, height=200)

def main():
    st.title("File Relocator")

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

    display_file_contents()

    num_lines = sum(1 for line in open('random_file.txt'))
    n = st.number_input("Line n:", min_value=1, max_value=num_lines, value=1, step=1)
    m = st.number_input("Line m:", min_value=1, max_value=num_lines, value=1, step=1)

    if st.button("Relocate"):
        if n == m:
            st.error("Error: Line n and Line m must have different values.")
        elif n - 1 == m:
            st.error("Error: Line n is already after Line m.")
        else:
            relocate_line(n, m)
            st.success(f"Line {n} relocated after Line {m}.")
        display_modified_file_contents()

    if st.button("Download Modified File"):
        with open('random_file.txt', 'r') as file:
            modified_file_contents = file.read()
        st.download_button("Download", data=modified_file_contents, file_name='random_file_modified.txt'

if __name__ == "__main__":
    main()
