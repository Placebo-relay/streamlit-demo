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
    for l, l_data in data:
        phi0_values, T_values = zip(*l_data)
        plt.plot(phi0_values, T_values, label=f"l = {l}")
    plt.xlabel("phi0")
    plt.ylabel("T")
    plt.legend()
    st.pyplot()

def calculate_and_display_data(a, b, z, l_values):
    phi0_values = np.linspace(a, b, 1000)
    data = save_data(l_values, phi0_values)
    
    if data:
        plot_data(data)
        
        for i, (l, l_data) in enumerate(data):
            st.sidebar.write(f"l = {l}")
            show_table = st.sidebar.checkbox(f"Show Table {i+1}", value=True)
            if show_table:
                st.table(l_data)

a = st.slider("a", 0.0, 10.0, 0.0, 0.1)
b = st.slider("b", 0.0, 10.0, 1.0, 0.1)
z = st.slider("z", 1, 10, 2)

l_values = set()
for _ in range(z):
    l = st.number_input("Enter the value for l")
    l_values.add(l)
    st.write(f"{z - len(l_values)} to go")

calculate_and_display_data(a, b, z, list(l_values))
