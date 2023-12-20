import numpy as np
from scipy.special import ellipk
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

def calculate_period(phi0, l):
    g = 9.8  # acceleration due to gravity
    T = 4 * np.sqrt(l / g) * ellipk(np.sin(np.deg2rad(phi0) / 2))
    return T

def save_data(l_values, phi0_values):
    data = []
    minT = np.inf  # Initialize minT with a large value
    maxT = -np.inf  # Initialize maxT with a small value
    
    for i, l in enumerate(l_values):
        l_data = []
        for phi0 in phi0_values:
            T = calculate_period(phi0, l)
            l_data.append((phi0, T))
            
            # Update minT and maxT if necessary
            minT = min(minT, T)
            maxT = max(maxT, T)
        
        data.append((l, l_data))
    
    return data, minT, maxT

def plot_data(data):
    fig, ax = plt.subplots()
    for l, l_data in data:
        phi0_values, T_values = zip(*l_data)
        ax.plot(phi0_values, T_values, label=f"l = {l}")
    ax.set_xlabel("phi0")
    ax.set_ylabel("T")
    ax.legend()
    return fig
    
def calculate_and_display_data(a, b, l_values):
    phi0_values = np.linspace(a, b, 1000)
    data, min_T, max_T = save_data(l_values, phi0_values)
    
    if data:
        st.write("global min_T, max_T:")
        st.write(min_T, max_T)
        fig = plot_data(data)
        st.pyplot(fig)
        
        for i, (l, l_data) in enumerate(data):

            # Create an expander for each DataFrame
            with st.sidebar.expander(f"Data l={l}"):
                st.write("global min_T, max_T")
                st.write(min_T, max_T)
                # DataFrame
                df = pd.DataFrame(l_data, columns=['phi0', 'T'])
                title_row = pd.DataFrame({'phi0': [f'range: {a,b}'], 'T': [f'T(phi0, l={l})']})
                df_with_title = pd.concat([title_row, df], ignore_index=True)
                

                # Display the DataFrame with the title/comment in Streamlit
                st.write(df_with_title)


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

st.title("Mathematical pendulum")
st.latex(r"T = 4 \sqrt{\frac{l}{g}} \cdot \text{ellipk}(\sin^2(\frac{\phi_0}{2}))")
# Define the bounds and step size
a_min = 0
a_max = 10
b_min = 0
b_max = 90
step = 1

# Create the dual-slider
a, b = st.slider("Angle Displacement", a_min, a_max, (0, 10), step=step)

# Convert the bounds to LaTeX format
a_latex = "0"
b_latex = r"10\degree"

# Display the dual-slider with pretty LaTeX bounds
st.latex(f"{a_latex} \leq \phi_0 \leq {b_latex}")

# Create a text area for user input
l_values_input = st.text_area("Enter l values (one per line)")

# Create a button to trigger the calculation
if st.button("Calculate"):
    # Check if the input is not empty
    if l_values_input.strip():
        # Split the input by newline
        lines = l_values_input.strip().split("\n")
        
        # Initialize a set to store unique valid values
        valid_values = set()
        
        # Iterate over each line and validate the value
        for line in lines:
            try:
                value = float(line)
                if value > 0:  # Take valid values
                    valid_values.add(value)
                else:
                    st.write(f"Invalid value: {line}")
            except ValueError:
                st.write(f"Invalid value: {line}")
        
        # Check if there are any valid values
        if valid_values:
            calculate_and_display_data(a, b, list(valid_values))
        else:
            st.write("No valid values entered.")
    else:
        st.write("Please enter some values.")
