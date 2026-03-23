import streamlit as st


@st.cache_data
def long_running_function(param1, param2):
    return '...'