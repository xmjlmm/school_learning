import streamlit as st

# 就是一个滑动模块， x的范围是0到100
# 然后显示x和x的平方，在滑动条的下面
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

# 就是一个按钮，然后原本是False, 点一下就变成True了
y = st.button('Click me!')
st.write(y)


# range没有到一百的，然后他就是可供选择的
z = st.selectbox('Which number is bigger?', list(range(1, 100)))
st.write('You selected', z)


# 就是输入一个名字点一个回车，然后没有后续了，是不是可以在后面在加点什么，比如滑块
# md 好像每个小组件都是一个独立的，互不影响
st.text_input("Your name", key="name")
# You can access the value at any point with:
st.session_state.name
