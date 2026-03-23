# import pandas as pd
# import streamlit as st
#
# def load_data(url):
#     df = pd.read_csv(url)  # 👈 Download the data
#     return df
#
# df = load_data("F:\\学习数据集\\datasets-master\\uber-rides-data1.csv")
# st.dataframe(df)
#
# st.button("Rerun")

import pandas as pd
import streamlit as st

# streamlit的缓存装饰器用来加速重复运行应用程序
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)  # 👈 Download the data
    return df

df = load_data("F:\\学习数据集\\datasets-master\\uber-rides-data1.csv")
st.dataframe(df)

st.button("Rerun")
