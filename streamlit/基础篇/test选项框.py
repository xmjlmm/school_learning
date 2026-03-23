# import streamlit as st
# import pandas as pd
#
# df = pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 20, 30, 40]
#     })
#
# option = st.selectbox(
#     'Which number do you like best?',
#     df['first column']
#     #  st.write(df['first column'])
# )
#
# 'You selected: ', option


import streamlit as st
import pandas as pd

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

if 'first column' in df:
    option = st.selectbox(
        'Please select a number from the first column',
         df['first column'])

    st.write('You selected: ', option)
else:
    st.error('Error: `first column` not found in DataFrame')
