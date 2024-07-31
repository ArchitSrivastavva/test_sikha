import streamlit as st
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from streamlit_dynamic_filters import DynamicFilters

# Define the correct password
correct_password = ")tut:5Z[bxU4"  # Replace with your desired password

# Create session state variables to manage authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'password_input' not in st.session_state:
    st.session_state.password_input = ''

# Create an empty container to handle the password input
password_container = st.empty()

if not st.session_state.authenticated:
    with password_container:
        st.session_state.password_input = st.text_input('Enter Password:', type='password')

        if st.session_state.password_input:
            if st.session_state.password_input == correct_password:
                st.session_state.authenticated = True
                password_container.empty()  # Clear the password container
                st.success("Password is correct! Access granted.")
            else:
                st.warning("Incorrect password. Please try again.")
else:
    st.session_state.password_input = ''  # Clear any leftover password input

# Run the rest of the app only if the user is authenticated
if st.session_state.authenticated:
    @st.cache_resource()
    def load_data():
        df = pd.read_csv("https://github.com/ArchitSrivastavva/test_sikha/blob/main/data2.csv")
        return df 

    st.title("Win Loss Reviews Feedback")

    df = load_data()

    df2 = df.groupby(['Market', 'Status', 'Size', 'year', 'MC Class']).agg({'combined': lambda x: ','.join(x)}).reset_index()

    df2['key'] = "Market=" + df2['Market'] + "; year=" + df2['year'].astype(str) + "; Status=" + df2['Status'] + "; DealSize=" + df2['Size'] + "; MC Class=" + df2['MC Class']

    dynamic_filters = DynamicFilters(df2, filters=['Market', 'Status', 'Size', 'year', 'MC Class', 'key'], filters_name='my_filters')
    
    with st.sidebar:
        st.write("Apply filters in any order 👇")
        dynamic_filters.display_filters(location='sidebar')

    new_df = dynamic_filters.filter_df()
    st.table(new_df['key'])
    st.text(str(new_df['combined'].values[0]))
    a = str(new_df['combined'].values[0])
    st.write(f"Country I live in is: {a}")
