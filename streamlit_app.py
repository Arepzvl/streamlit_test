import streamlit as st

# Set the app title
st.title('Unit Converter')

# Add a welcome message
st.write('Welcome to the Unit Converter App!')

# Create a text input for a custom message
widgetuser_input = st.text_input('Enter a custom message:', 'Hello, Streamlit!')
st.write('Customized Message:', widgetuser_input)

# Unit types (you can add more categories like mass, temperature, etc.)
unit_category = st.selectbox('Select a unit category:', ['Length'])

# Define units and their conversion factors (relative to base unit: meter)
length_units = {
    'Meter (m)': 1.0,
    'Kilometer (km)': 1000.0,
    'Centimeter (cm)': 0.01,
    'Millimeter (mm)': 0.001,
    'Mile (mi)': 1609.34,
    'Yard (yd)': 0.9144,
    'Foot (ft)': 0.3048,
    'Inch (in)': 0.0254
}

# Show length unit converter
if unit_category == 'Length':
    from_unit = st.selectbox('From Unit:', list(length_units.keys()))
    to_unit = st.selectbox('To Unit:', list(length_units.keys()))
    value = st.number_input('Enter value to convert:', min_value=0.0, value=1.0)

    # Convert the value
    result = value * length_units[from_unit] / length_units[to_unit]

    # Display the result
    st.write(f'{value} {from_unit} is equal to {result:.4f} {to_unit}')
