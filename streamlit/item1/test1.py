import streamlit as st
import pandas as pd


st.write('''
# hello world

this is a hello world app
''')

source = pd.read_csv('/pythonProject/streamlit/item1/a.csv')
# print(source)
st.line_chart(source)


