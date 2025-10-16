import streamlit as st
import numpy as np
height = st.text_input("请输入身高(cm)", "190")
height = np.float64(height) / 100

weight = st.text_input("请输入体重(kg)", "190")
weight = np.float64(weight)

BMI = weight / height ** 2

st.write(BMI)