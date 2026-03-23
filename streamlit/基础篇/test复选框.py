import streamlit as st
import numpy as np
import pandas as pd

# 就是给你一个框，影藏数据，你点这个框数据就出来了
if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])
    # 就是要缩进，记得，因为如果条件没过，都不会产生chart_data
    # st.write() 发现可有可无，变成了jupyter里面魔法代码的感觉了
    # chart_data

    st.write(chart_data)
