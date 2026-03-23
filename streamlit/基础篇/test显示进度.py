import streamlit as st
import time

'Starting a long computation...'

# Add a placeholder
# 就是一个占位符，在计算的时候，显示进度条，默认是从0开始的
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    # Update the progress bar with each iteration.
    latest_iteration.text(f'Iteration {i+1}')
    # progress就是进度条
    bar.progress(i + 1)
    time.sleep(0.1)

# \'转义字符
'...and now we\'re done!'


