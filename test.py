import streamlit as st
import pandas as pd

st.title('版面示範')

df = pd.DataFrame({
    '國文': [98, 76, 100, 38, 40],
    '數學': [80, 46, 80, 67, 66]
})

# 建立兩個欄位，左右並排
col1, col2 = st.columns(2)

with col1:
    st.subheader('國文成績')
    st.dataframe(df[['國文']])

with col2:
    st.subheader('數學成績')
    st.dataframe(df[['數學']])
