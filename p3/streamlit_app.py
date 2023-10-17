import streamlit as st
from streamlit import file_uploader
import random
from googletrans import Translator

def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

# Translate the text strings
st.title(translate_text("Line Relocator", "ja"))

st.sidebar.title(translate_text("Options", "ja"))
option = st.sidebar.radio(translate_text("Select an option:", "ja"), (translate_text("Generate Random File", "ja"), translate_text("Upload File", "ja")))

file_path = 'original_file.txt'
modified_file_path = 'file_modified.txt'
log_file_path = 'relocation_log.txt'

if option == translate_text("Generate Random File", "ja"):
    num_lines = st.sidebar.slider(translate_text("Number of Lines", "ja"), 5, 10, 5)
    generate_random_file(file_path, num_lines)
    st.success(translate_text(f"Generated random file with {num_lines} lines.", "ja"))
    with open(log_file_path, 'w') as file:
        file.write(translate_text("Relocation Log:\n", "ja"))

elif option == translate_text("Upload File", "ja"):
    uploaded_file = st.sidebar.file_uploader(translate_text("Upload a file", "ja"))
    if uploaded_file is not None:
        file_contents = uploaded_file.read()
        with open(file_path, 'wb') as file:
            file.write(file_contents)
        st.success(translate_text("Uploaded file successfully.", "ja"))
        with open(log_file_path, 'w') as file:
            file.write(translate_text("Relocation Log:\n", "ja"))

display_file_contents(file_path)

num_lines = sum(1 for line in open(file_path))
n = st.number_input(translate_text("Line n:", "ja"), min_value=1, max_value=num_lines, value=1, step=1)
m = st.number_input(translate_text("Line m:", "ja"), min_value=1, max_value=num_lines, value=1, step=1)

if st.button(translate_text("Relocate", "ja")):
    if n == m:
        st.error(translate_text("Error: Line n and Line m must have different values.", "ja"))
    elif n - 1 == m:
        st.error(translate_text("Error: Line n is already after Line m.", "ja"))
    else:
        relocate_line(file_path, modified_file_path, n, m, log_file_path)
        st.success(translate_text(f"Line {n} relocated after Line {m}.", "ja"))
        display_modified_file_contents(modified_file_path)

if st.button(translate_text("Prepare file for download", "ja")):
    with open(modified_file_path, 'r') as file:
        modified_file_contents = file.read()
    st.download_button(translate_text("Download", "ja"), data=modified_file_contents, file_name=modified_file_path)

display_relocation_log(log_file_path)

# Add language options
language_options = {
    "Japanese": "ja",
    "Russian": "ru",
    "German": "de",
    "French": "fr"
}

selected_language = st.sidebar.selectbox("Select Language", list(language_options.keys()))

if st.sidebar.button("Translate"):
    target_language = language_options[selected_language]
    st.title(translate_text("Line Relocator", target_language))
    st.sidebar.title(translate_text("Options", target_language))
    option = st.sidebar.radio(translate_text("Select an option:", target_language), (
        translate_text("Generate Random File", target_language),
        translate_text("Upload File", target_language)
    ))

    # Rest of the code remains the same
