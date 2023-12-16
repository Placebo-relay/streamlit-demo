
import streamlit as st
import altair as alt
import numpy as np
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

st.title("Dynamics of a material point")
st.markdown("## Free descent of 🚡")
st.markdown("### > 👈 sidebar: ℹ️+🍎")
st.markdown("🎨: Position🔵, Velocity🔴")


image_url = "p5/FORCES.png"
image = st.sidebar.image(image_url, caption='Forces layout 🍎', use_column_width=True)

# Sidebar widgets
st.sidebar.title("Parameters ℹ️")
mu = st.sidebar.number_input("Coefficient of friction", value=430, min_value=300, max_value=1000)
m = st.sidebar.number_input("Mass", value=500, min_value=100, max_value=1000)
U = st.sidebar.number_input("Environmental force", value=3, min_value=1, max_value=10)
g = st.sidebar.number_input("Acceleration due to gravity", value=9.8, min_value=9.0, max_value=10.0)
k = st.sidebar.number_input("Constant factor characteristic of the spring", value=6100, min_value=3000, max_value=10000)
v0 = st.sidebar.number_input("Initial velocity", value=1.8, min_value=0.3, max_value=10.0)
gamma = st.sidebar.number_input("Gamma, misaligned coefficient", value=0.14, min_value=0.01, max_value=1.0)
alpha = st.sidebar.number_input("Alpha angle, in grad", value=10.0, min_value=5.0, max_value=45.0, step=0.5)
U_angle = st.sidebar.number_input("U angle, in grad", value=15.0, min_value=-15.0, max_value=15.0, step=0.5)

# Equations
a_x = lambda vel_x, vel_y, y: -mu * vel_x / m + mu*U*np.cos(np.radians(U_angle - alpha))/m + g*np.sin(np.radians(alpha))
a_y = lambda vel_x, vel_y, y: -mu * vel_y / m - k * y / m - mu*U*np.sin(np.radians(U_angle - alpha))/m - g*np.cos(np.radians(alpha))

# Calculate the typical transition time
tx = abs((-1 - 0) / (mu/m))
tt = abs((-1 - k/m) / (mu/m))
typical_transition_time = max(tx, tt)

# target
target_y = (- mu*U*np.sin(np.radians(U_angle - alpha))/m - g*np.cos(np.radians(alpha)) ) *m / k
target_vx = mu*U*np.cos(np.radians(U_angle - alpha))/m + g*np.sin(np.radians(alpha)) * m / mu

# Initial conditions
x = 0
y = gamma * (- mu*U*np.sin(np.radians(U_angle - alpha))/m - g*np.cos(np.radians(alpha)) ) *m /k
vel_x = -v0 * np.sin(np.radians(alpha))
vel_y = v0 * np.cos(np.radians(alpha))

# Time step and duration
dt = 1 / typical_transition_time / 24  # Choose an appropriate time step
duration = typical_transition_time  # Duration of simulation in seconds

# Lists to store position values
time = []
position_x = []
position_y = []
position_vx = []
position_vy = []

# Simulation loop
for t in range(int(duration / dt)):
    # Calculate acceleration
    a_x_val = a_x(vel_x, vel_y, y)
    a_y_val = a_y(vel_x, vel_y, y)

    # Update velocity
    vel_x += a_x_val * dt
    vel_y += a_y_val * dt

    # Update position
    x += vel_x * dt
    y += vel_y * dt

    # Store position values
    time.append(t * dt)
    position_x.append(x)
    position_y.append(y)
    position_vx.append(vel_x)
    position_vy.append(vel_y)

# Create DataFrame for plotting
data = pd.DataFrame({
    'Time': time,
    'Position X': position_x,
    'Position Y': position_y,
    'Velocity X': position_vx,
    'Velocity Y': position_vy,
    'Target X': [target_vx * t for t in time],
    'Target Y': [target_y] * len(time),
    'Target Velocity X': [target_vx] * len(time),
    'Target Velocity Y': [0] * len(time)
    })

# Plotting states
chart_y = alt.Chart(data).mark_line().encode(
    x='Time',
    y='Position Y',
    color=alt.value('blue'),
    tooltip=['Time', 'Position Y', 'Target Y']
).properties(
    title='Y-axis'
)

# Add Velocity Y line to the chart
chart_y += alt.Chart(data).mark_line().encode(
    x='Time',
    y='Velocity Y',
    color=alt.value('red'),
    tooltip=['Time', 'Velocity Y', 'Target Velocity Y']
)

# Add Target Y line as a dotted line
chart_y += alt.Chart(data).mark_line(strokeDash=[5, 5]).encode(
    x='Time',
    y='Target Y',
    color=alt.value('cyan'),
    tooltip=['Time', 'Target Y', 'Position Y']
)

# Add Target Velocity Y line as a dotted line
chart_y += alt.Chart(data).mark_line(strokeDash=[5, 5]).encode(
    x='Time',
    y='Target Velocity Y',
    color=alt.value('yellow'),
    tooltip=['Time', 'Target Velocity Y', 'Velocity Y']
)

chart_x = alt.Chart(data).mark_line().encode(
    x='Time',
    y='Position X',
    color=alt.value('blue'),
    tooltip=['Time', 'Position X', 'Target X']
).properties(
    title=alt.TitleParams(text='X-axis', anchor='end')
)

# Add Velocity X line to the chart
chart_x += alt.Chart(data).mark_line().encode(
    x='Time',
    y='Velocity X',
    color=alt.value('red'),
    tooltip=['Time', 'Velocity X', 'Target Velocity X']
)

# Add Target X line as a dotted line
chart_x += alt.Chart(data).mark_line(strokeDash=[5, 5]).encode(
    x='Time',
    y='Target X',
    color=alt.value('cyan'),
    tooltip=['Time', 'Target X', 'Position X']
)

# Add Target Velocity X line as a dotted line
chart_x += alt.Chart(data).mark_line(strokeDash=[5, 5]).encode(
    x='Time',
    y='Target Velocity X',
    color=alt.value('yellow'),
    tooltip=['Time', 'Target Velocity X', 'Velocity X']
)

chart_yx = alt.Chart(data).mark_line().encode(
    x='Position X',
    y='Position Y',
    color=alt.value('blue'),
    tooltip=['Time', 'Position X', 'Target X', 'Position Y', 'Target Y']
).properties(
    title='Plot y(x)'
)

chart_yx += alt.Chart(data).mark_line(strokeDash=[5, 5]).encode(
    x='Position X',
    y='Target Y',
    color=alt.value('cyan'),
    tooltip=['Time', 'Target X', 'Position X', 'Target Y' , 'Position Y']
)

st.altair_chart(chart_y, use_container_width=True)
st.altair_chart(chart_x, use_container_width=True)
st.altair_chart(chart_yx, use_container_width=True)