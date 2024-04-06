import streamlit as st
# 在侧边栏中添加导航链接
st.sidebar.title("导航")
st.sidebar.page_link("pages/upload_file.py", label="上传文件")
st.sidebar.page_link("pages/chatbot.py", label="聊天窗口")


if st.sidebar.button("Logout"):
    st.switch_page("login.py")