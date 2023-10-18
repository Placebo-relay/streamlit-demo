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

def plot_data(data):
    fig, ax = plt.subplots()
    for l, l_data in data:
        phi0_values, T_values = zip(*l_data)
        ax.plot(phi0_values, T_values, label=f"l = {l}")
    ax.set_xlabel("phi0")
    ax.set_ylabel("T")
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

#a = st.slider("a", 0.0, 10.0, 0.0, 0.1)
#b = st.slider("b", 0.0, 10.0, 1.0, 0.1)
st.latex(r"T = 4 \sqrt{\frac{l}{g}} \cdot \text{ellipk}(\sin^2(\frac{\phi_0}{2}))")

a, b = st.slider("angle", -0.5 * 3.14159, 0.5 * 3.14159, (-0.5 * 3.14159, 1.0), 0.1)

# Convert the bounds to LaTeX format
a_latex = r"\frac{-\pi}{2}"
b_latex = r"\frac{\pi}{2}"

# Display the dual-slider with pretty LaTeX bounds
st.latex(f"{a_latex} \leq \phi_0 \leq {b_latex}")
#z = st.slider("z", 1, 10, 2)

l_values_input = st.text_area("Enter the values for l (one value per line)", "")
l_values = set(map(float, l_values_input.strip().split("\n")))

calculate_and_display_data(a, b, list(l_values)) #z
