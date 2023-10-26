import numpy as np
from scipy.special import ellipk
import matplotlib.pyplot as plt
import streamlit as st


def calculate_period(phi0, l, g):
    T = 4 * np.sqrt(l / g) * ellipk(np.sin(phi0 / 2) ** 2)
    return T


def save_data(l_values, phi0_values, g):
    data = []
    for l in l_values:
        l_data = []
        for phi0 in phi0_values:
            T = calculate_period(phi0, l, g)
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


def calculate_and_save_data(a, b, l_values, g):
    phi0_values = np.linspace(a, b, 1000)
    data = save_data(l_values, phi0_values, g)

    if data:
        fig = plot_data(data)
        st.pyplot(fig)

        for i, (l, l_data) in enumerate(data):
            fig, ax = plt.subplots()
            phi0_values, T_values = zip(*l_data)
            ax.plot(phi0_values, T_values)
            ax.set_xlabel("phi0")
            ax.set_ylabel("T")
            ax.set_title(f"l = {l}")
            st.pyplot(fig)

            with open(f"{i+1}.txt", "w") as file:
                file.write(f"#l = {l}\n")
                for phi0, T in l_data:
                    file.write(f"{phi0}\t{T}\n")


def get_float_input(prompt, min_value, max_value, default_value):
    value = st.text_input(prompt, default_value)
    if value == "":
        value = default_value
    else:
        while True:
            try:
                value = float(value)
                if value < min_value or value > max_value:
                    raise ValueError
                break
            except ValueError:
                st.error("Invalid value entered.")
                value = st.text_input(prompt, default_value)
    return value


def get_int_input(prompt, min_value):
    value = st.text_input(prompt)
    while True:
        try:
            value = int(value)
            if value <= min_value:
                raise ValueError
            break
        except ValueError:
            st.error("Invalid value entered.")
            value = st.text_input(prompt)
    return value


def get_l_values(num_l):
    l_values = []
    while len(l_values) < num_l:
        l = get_float_input(f"Enter l value {len(l_values)+1}: ", 0, float("inf"), None)
        if l not in l_values:
            l_values.append(l)
        else:
            st.warning(f"Ignoring repeat {l}")
        st.info(f"l values are: {l_values}")
    return l_values


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
    
    st.title("Pendulum Period Calculator")
    st.write("This app calculates and visualizes the period of a pendulum for different combinations of l and phi0.")

    a_min = -np.pi / 2
    a_max = np.pi / 2
    b_min = 0.0
    b_max = np.pi / 2

    a = get_float_input(f"Enter the lower bound for phi0 (hit Enter for {a_min}): ", a_min, a_max, a_min)
    b = get_float_input(f"Enter the upper bound for phi0 (hit Enter for {b_max}): ", b_min, b_max, b_max)
    if a > b:
        a, b = b, a

    num_l = get_int_input("Enter the number of l values: ", 0)
    l_values = get_l_values(num_l)

    calculate_and_save_data(a, b, l_values, 9.8)
    st.success("Calculation and visualization complete. Plots are displayed above.")


if __name__ == "__main__":
    main()
