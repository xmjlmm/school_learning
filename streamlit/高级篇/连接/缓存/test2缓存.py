import pandas as pd
import streamlit as st
import numpy as np

@st.cache_data
def transform(df):
    df = df.filter(items=['x1', 'x2'])
    df = df.apply(np.sum, axis=0)
    return df


df = pd.read_csv("F:\\学习数据集\\datasets-master\\3d-scatter.csv")
print(df)
df = transform(df)
st.divider()
st.dataframe(df)
st.divider()
st.bar_chart(df)

st.line_chart(df)

import math
x = math.atan(1/20)
print(x)