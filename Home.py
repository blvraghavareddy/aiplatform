import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
import json

st.set_page_config(page_title='AI Disease Prediction Platform', layout='centered',page_icon='👨‍⚕️')
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

logo = load_lottiefile("h.json")

st.title("AI Disease Prediction Platform")
c1,c2,c3 = st.columns([1,1,1])
with c2:
    st_lottie(logo, speed=1, width=200, height=200, key="initial")

# Load the data
df = pd.read_csv('user_data.csv')
username_input = st.text_input("Enter the username: ")
co1, co2 = st.columns(2)
# Get user input for the username
with co1:
    dashboard_button = st.button('Display Dashboard')
with co2:
    delete_button = st.button('Delete Data')

# Convert the 'Username' column to string type
df['Username'] = df['Username'].astype(str)

# Filter the DataFrame to get data for the entered username
user_data = df[df['Username'] == username_input]
if username_input == '':
    st.info('👆 Enter a username.')
    st.warning('👈 Record the Asthma symptoms to generate the dashboard in sidebar.')
# Check if any data exists for the entered username
if username_input is not None and len(user_data) > 0:
    # Convert the 'Date' column to datetime type
    user_data['Date'] = pd.to_datetime(user_data['Date'])

    # Extract only the date part and convert it to string
    user_data['Date'] = user_data['Date'].dt.date.astype(str)

    # Sort the DataFrame based on the 'Date' column
    user_data = user_data.sort_values(by='Date')

    # Plot the data using Streamlit line chart
    

    # Delete data if button is clicked
    if delete_button:
        # Remove data associated with the entered username
        df = df[df['Username'] != username_input]
        st.info(f"Data for username '{username_input}' has been deleted.")

# Display the dashboard button
if dashboard_button:
    # Show additional statistics or visualizations
    if len(user_data) == 0:
        st.warning('⚠️ No data available for the entered username.')
        st.info('👈 Record the Asthma symptoms to generate the dashboard in sidebar.')
    else:
        st.line_chart(user_data.set_index('Date')['Severity'])
    

# Save the modified DataFrame back to the CSV file
df.to_csv('user_data.csv', index=False)
