import streamlit as st

st.sidebar.title("导航")
st.sidebar.page_link("pages/upload_file.py", label="上传文件")
st.sidebar.page_link("pages/chatbot.py", label="聊天窗口")

# st.write("这是个人资料页面")

uploaded_file = st.file_uploader("Choose a PDF file", accept_multiple_files=False, type=['pdf'])
if uploaded_file is not None:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    # st.write(bytes_data)

if st.sidebar.button("Logout"):
    st.switch_page("login.py")
