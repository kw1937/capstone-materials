import streamlit as st

st.title("정비 자재 검색 시스템")

work_name = st.text_input("작업명을 입력하세요")

if work_name:
    st.write("검색한 작업:", work_name)

