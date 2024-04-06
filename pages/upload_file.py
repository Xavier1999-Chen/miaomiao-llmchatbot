import streamlit as st

st.sidebar.title("导航")
st.sidebar.page_link("pages/upload_file.py", label="上传文件")
st.sidebar.page_link("pages/chatbot.py", label="聊天窗口")

st.write("这是个人资料页面")

if st.sidebar.button("Logout"):
    st.switch_page("login.py")