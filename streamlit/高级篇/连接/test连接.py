import streamlit as st

conn = st.connection("secret.toml")
df = conn.query("select * from data_learn")
st.dataframe(df)