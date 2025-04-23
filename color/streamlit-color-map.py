import streamlit as st
import numpy as np
from scipy.ndimage import label
import pandas as pd

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
    visibility: visible;
}
footer:after{
    visibility: visible;
    Content:"Demo for Technologies of Programming. Copyright @ 2023";
    display: block;
    position: relative;
    padding: 5px;
    top:3px;
    color: tomato;
    text-align: left;
</style>
"""
st.markdown(hide_menu, unsafe_allow_html=True)

st.title('Max Area-of-same')

@st.cache_data
def generate_emoji_matrix(rows, cols, choice_key):
    # Generate random emoji matrix
    emoji_matrix = np.random.choice(choice, size=(rows, cols))
    return emoji_matrix

def find_largest_area(emoji_matrix, emoji):
    # Convert emoji matrix to binary matrix
    binary_matrix = np.where(emoji_matrix == emoji, 1, 0)

    # Label connected components
    labeled_matrix, num_labels = label(binary_matrix)

    # Check if there are any labeled areas
    if num_labels == 0:
        return 0, None

    # Count the size of each labeled area
    area_sizes = np.bincount(labeled_matrix.flatten())[1:]
    # labeled_matrix #PRINT to display how it works
    # Find the largest area
    largest_area_size = np.max(area_sizes)
    largest_area_emoji = emoji_matrix[labeled_matrix == np.argmax(area_sizes) + 1][0]

    return largest_area_size, largest_area_emoji


choice1 = ['🟥', '🟩', '🟦', '🟨', '🟧', '🟪', '🟫', '⬜', '⬛']
choice2 = ["😀", "🥶", "😍", "👿", "😭", "🤪", "🤮", "😴"]
choice3 = ["1", "2", "3", "4", "5", "6","7"]
choice0 = ["🎲", "🚀", "🎁","👻","🎄","🦀","👾", "🐍", "🔥", "🌊"]

my_dict = {
    'x10 Emojis 🎲': choice0,
    'x9 Colors 🟥': choice1,
    'x8 Face Emojis 😀': choice2,
    'x7 Plain Numbers 123': choice3
}

st.markdown("### >👈 Use sidebar for 🕹️")

# SIDEBAR >
with st.sidebar:
    st.title("Options 🕹️")
    choice_key = st.radio("Choose ✔️", list(my_dict.keys()))
    choice = my_dict[choice_key]
    
    highlight_toggle = st.checkbox("Highlight 🖌", value=True)
    
    st.subheader("Cache 💾")
    if st.button("Clear Cache 🗑️"):
        st.cache_data.clear()

    st.subheader("Resize 📐")
    rows = st.number_input("↕ Rows:", value=5, min_value=1, max_value=10, step=1)
    cols = st.number_input("↔ Columns:", value=5, min_value=1, max_value=10, step=1)


# Generate emoji matrix
emoji_matrix = generate_emoji_matrix(rows, cols, choice_key)

# Calc
emojis = set(i for j in emoji_matrix for i in j)
min_area_size = float('inf')
min_area_emoji = set()
max_area_size = 0
max_area_emoji = set()

for emoji in emojis:
    # Find the largest area for each emoji
    largest_area_size, largest_area_emoji = find_largest_area(emoji_matrix, emoji)
    
    # Update min and max area if necessary
    if largest_area_size < min_area_size:
        min_area_size = largest_area_size
        min_area_emoji = set(largest_area_emoji)
    if largest_area_size == min_area_size:
        min_area_size = largest_area_size
        min_area_emoji.add(largest_area_emoji)
    if largest_area_size > max_area_size:
        max_area_size = largest_area_size
        max_area_emoji = set(largest_area_emoji)
    if largest_area_size == max_area_size:
        max_area_emoji.add(largest_area_emoji)


col1, col2, col3   = st.columns([1,1,3])

# External toggle
with col1:    
    if st.button("Unsafe Clear 🗑️"):
        st.cache_data.clear()
        st.write('🗑️ = 🎲')

with col2:
    if highlight_toggle:
        selected_item = st.selectbox("Highlight 🖌️", choice)
        np_tuple = find_largest_area(emoji_matrix, selected_item)
        py_tuple = tuple(item.item() if isinstance(item, np.generic) else str(item) for item in np_tuple)
        st.write(py_tuple)

        
emoji_matrix = pd.DataFrame(emoji_matrix)

# Display DataFrame with highlighting
if highlight_toggle:
    highlighted_df = emoji_matrix.style.apply(lambda x: ['background-color: yellow' if item == selected_item else '' for item in x], axis=1)
    st.dataframe(highlighted_df)
else:
    st.dataframe(emoji_matrix)

# Print the result
st.markdown("### Stats 📊")

py_maxlist = tuple(item.item() if isinstance(item, np.generic) else str(item) for item in max_area_emoji)
st.write(f"The largest area size is {max_area_size} by {py_maxlist}")
if (min_area_size != max_area_size):
    py_minlist = tuple(item.item() if isinstance(item, np.generic) else str(item) for item in min_area_emoji)
    st.write(f"The smallest area size is {min_area_size} by {py_minlist}")
else:
     st.write(f"The smallest area size = largest")

with col1:
    for _ in max_area_emoji:
        st.write(_)
with col2:
    for _ in min_area_emoji:
        st.write(_)

st.markdown("### 🐍Code snapshot✂️")

body = """


def find_largest_area(emoji_matrix, emoji):
    # Convert emoji matrix to binary matrix
    binary_matrix = np.where(emoji_matrix == emoji, 1, 0)

    # Label connected components manually
    labeled_matrix = np.zeros_like(binary_matrix)
    current_label = 1

    for i in range(binary_matrix.shape[0]):
        for j in range(binary_matrix.shape[1]):

	# MAIN: if not labeled in labeled_matrix, and is 1 in binary

            if binary_matrix[i, j] == 1 and labeled_matrix[i, j] == 0:

		# INIT STACK
                stack = [(i, j)]
                labeled_matrix[i, j] = current_label

                while stack:
                # EXPLORE NEIGHBORHOOD OF LAST ADDED, POP IT
                    x, y = stack.pop()

                    neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
                    
                    # ITERATE over neigbors
                    for neighbor in neighbors:
                        nx, ny = neighbor
                        x_in_range = (0 <= nx < binary_matrix.shape[0])
                        y_in_range = (0 <= ny < binary_matrix.shape[1])
                        if x_in_range and y_in_range:
                        # ADD TO STACK IF not yet labeled AND is 1
                            is_one = (binary_matrix[nx, ny] == 1)
                            is_labeled = (labeled_matrix[nx, ny] == 0)
                            if is_one and is_labeled:
                                stack.append((nx, ny))
                                labeled_matrix[nx, ny] = current_label

                current_label += 1

    # Check if there are any labeled areas
    num_labels = current_label - 1
    if num_labels == 0:
        return 0

    # Count the size of each labeled area (111 22 3333)
    area_sizes = np.bincount(labeled_matrix.flatten())[1:]

    # Find the largest area
    largest_area_size = np.max(area_sizes)

    return largest_area_size
            """
            
st.code(body, language="python", line_numbers=False)
