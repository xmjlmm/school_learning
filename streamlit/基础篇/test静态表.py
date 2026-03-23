import streamlit as st
import numpy as np
import pandas as pd

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % (i+1) for i in range(20)))
# st.table(dataframe)

st.table(dataframe.style.highlight_max(axis = 0))