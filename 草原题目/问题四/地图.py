import streamlit as st
import numpy as np
import pandas as pd

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)


map_data_2 = pd.DataFrame(
    np.random.randn(10000, 2) / [50, 50] + [39.9, 116.4],
    columns = ['lat', 'lon']
)
st.map(map_data_2)