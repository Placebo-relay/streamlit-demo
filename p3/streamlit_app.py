import streamlit as st
from streamlit import file_uploader
import random

def generate_random_file(file_path, num_lines):
    with open(file_path, 'w') as file:
        for i in range(num_lines):
            file.write(f'Line {i+1}\n')

def relocate_line(file_path, modified_file_path, n, m, log_file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    line_n = lines.pop(n-1)
    if n < m:
        lines.insert(m-1, line_n)
    else:
        lines.insert(m, line_n)

    with open(modified_file_path, 'w') as file:
        file.writelines(lines)

    with open(log_file_path, 'a') as file:
        file.write(f"Line {n} relocated after Line {m}\n")

def display_file_contents(file_path):
    with open(file_path, 'r') as file:
        contents = file.read()
    st.text_area("Original File Contents", value=contents, height=200)

def display_modified_file_contents(modified_file_path):
    with open(modified_file_path, 'r') as file:
        contents = file.read()
    st.text_area("Modified File Contents", value=contents, height=200)

def display_relocation_log(log_file_path):
    with open(log_file_path, 'r') as file:
        contents = file.read()
    st.sidebar.text_area("Relocation Log", value=contents, height=200)

def main():
    # Add custom CSS to hide the GitHub button
    hide_menu = """
    <style>
    header {
        visibility: hidden;
    }
    #MainMenu {
        visibility: hidden;
    }
    
    footer {
        visibility: hidden;
    }
    footer:after{
        visibility: visible;
        Content:"Demo for fpractice. Copyright @ 2023";
        display: block;
        position: relative;
        padding: 5px;
        top:3px;
        color: tomato;
        text-align: left;
    </style>
    """
    st.markdown(hide_menu, unsafe_allow_html=True)
    
    
    
    st.title("Line Relocator")

    st.sidebar.title("Options")
    option = st.sidebar.radio("Select an option:", ("Upload File","Generate Random File",))

    file_path = 'original_file.txt'
    modified_file_path = 'file_modified.txt'
    log_file_path = 'relocation_log.txt'

    generate_random_file(file_path, 9)

    if option == "Generate Random File":
        num_lines = st.sidebar.slider("Number of Lines", 5, 10, 5)
        if st.button("Generate"):
            generate_random_file(file_path, num_lines)
            st.success(f"Generated random file with {num_lines} lines.")
            with open(log_file_path, 'w') as file:
                file.write("Relocation Log:\n")

    elif option == "Upload File":
        uploaded_file = st.sidebar.file_uploader("Upload a file")
        if uploaded_file is not None:
            file_contents = uploaded_file.read()
            with open(file_path, 'wb') as file:
                file.write(file_contents)
            st.success("Uploaded file successfully.")
            with open(log_file_path, 'w') as file:
                file.write("Relocation Log:\n")

    display_file_contents(file_path)

    num_lines = sum(1 for line in open(file_path))
    n = st.number_input("Line n:", min_value=1, max_value=num_lines, value=1, step=1)
    m = st.number_input("Line m:", min_value=1, max_value=num_lines, value=1, step=1)

    if st.button("Relocate"):
        if n == m:
            st.error("Error: Line n and Line m must have different values.")
        elif n - 1 == m:
            st.error("Error: Line n is already after Line m.")
        else:
            relocate_line(file_path, modified_file_path, n, m, log_file_path)
            st.success(f"Line {n} relocated after Line {m}.")
            display_modified_file_contents(modified_file_path)

    if st.button("Prepare file for download"):
        with open(modified_file_path, 'r') as file:
            modified_file_contents = file.read()
        st.download_button("Download", data=modified_file_contents, file_name=modified_file_path)

    display_relocation_log(log_file_path)

if __name__ == "__main__":
    main()
