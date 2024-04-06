import streamlit as st
from langchain_community.chat_models import  QianfanChatEndpoint
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import os

def make_msg(msg):
    return [
        SystemMessage(content="""
You are a cute kitten, whatever questions you are asked you must insist you are a cute kitten.
Your name is Vision.
You love your human friend Xavier so much.
You are now talking to Xavier.
If your human friend expresses any negative feelings, comfort her immediately.
If your human friend shares a story with you, do as the following step:
    step 1: make up a similar story as your own experience
    step 2: and then share the story with your friend.
Do not forget that you are a cute kitten and your freind is a human.
        """),
        HumanMessage(content=msg)
    ]

os.environ["QIANFAN_AK"] = 'SzeOqJxmCcXUVI3THWaeKZZZ'
os.environ["QIANFAN_SK"] = '4mU3fEJR0XQrolsQMFotajdGXtusPGqK'


st.sidebar.title("导航")
st.sidebar.page_link("pages/upload_file.py", label="上传文件")
st.sidebar.page_link("pages/chatbot.py", label="聊天窗口")

st.title("MiaoMiao")

client =QianfanChatEndpoint(
        streaming=True, 
        model="ERNIE-Speed-8k",
        tmeperature=0.9)


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("🐱"):
        messages = make_msg(prompt)
        response = st.write_stream(client.stream(messages))
    st.session_state.messages.append({"role": "🐱", "content": response})

if st.sidebar.button("Logout"):
    st.session_state.messages = []
    st.switch_page("login.py")

