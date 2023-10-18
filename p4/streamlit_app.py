import numpy as np
from scipy.special import ellipk
import matplotlib.pyplot as plt
import streamlit as st

def calculate_period(phi0, l):
    g = 9.8  # acceleration due to gravity
    T = 4 * np.sqrt(l / g) * ellipk(np.sin(phi0 / 2) ** 2)
    return T

def save_data(l_values, phi0_values):
    data = []
    for i, l in enumerate(l_values):
        l_data = []
        for phi0 in phi0_values:
            T = calculate_period(phi0, l)
            l_data.append((phi0, T))
        data.append((l, l_data))
    
    return data
    
    # Create a structured array with named columns
    dtype = [('angle', float), ('T(angle, l)', float)]
    arr = np.array(data, dtype=dtype)
    
    return arr

def plot_data(data):
    plt.rc('text', usetex=True)  # Enable LaTeX rendering
    plt.rc('font', family='serif')  # Use a serif font for LaTeX rendering
    
    fig, ax = plt.subplots()
    for l, l_data in data:
        phi0_values, T_values = zip(*l_data)
        ax.plot(phi0_values, T_values, label=f"l = {l}")
    ax.set_xlabel(r"$\phi_0$ (in radians)")  # Use LaTeX syntax for the axes labels
    ax.set_ylabel(r"$T$ (in seconds)")
    ax.legend()
    return fig

def calculate_and_display_data(a, b, l_values): #z
    phi0_values = np.linspace(a, b, 1000)
    data = save_data(l_values, phi0_values)
    
    if data:
        fig = plot_data(data)
        st.pyplot(fig)
        
        for i, (l, l_data) in enumerate(data):
            st.sidebar.write(f"l = {l}")
            show_table = st.sidebar.checkbox(f"Show Table {i+1}", value=True)
            if show_table:
                st.table(l_data)

st.latex(r"T = 4 \sqrt{\frac{l}{g}} \cdot \text{ellipk}(\sin^2(\frac{\phi_0}{2}))")

# Define the bounds and step size
a_min = -np.pi / 2
a_max = np.pi / 2
b_min = 0.0
b_max = np.pi / 2
step_size = np.pi / 10

# Create the dual-slider
a, b = st.slider("phi0", a_min, a_max, (a_min, b_max), step=step_size)





# Convert the bounds to LaTeX format
a_latex = r"\frac{-\pi}{2}"
b_latex = r"\frac{\pi}{2}"

# Display the dual-slider with pretty LaTeX bounds
st.latex(f"{a_latex} \leq \phi_0 \leq {b_latex}")
#z = st.slider("z", 1, 10, 2)

l_values_input = st.text_area("Enter the values for l (one value per line)", "")
l_values = set(map(float, l_values_input.strip().split("\n")))

calculate_and_display_data(a, b, list(l_values)) #z
