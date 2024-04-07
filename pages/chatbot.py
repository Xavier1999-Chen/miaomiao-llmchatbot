import streamlit as st
from langchain_community.chat_models import  QianfanChatEndpoint
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import os
import re
import time
import random

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

chat_title = st.title("MiaoMiao")

chat_win = st.empty()
chat_input = st.empty()
client =QianfanChatEndpoint(
        streaming=True, 
        model="ERNIE-Speed-8k",
        tmeperature=0.9)

with chat_win.container(height=500):
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := chat_input.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        chat_title.title("正在输入……")
        messages = make_msg(prompt)
        response = client.invoke(messages)
        response = response.content
        sentences = re.split(r'[，。,.]', response)
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
        # print(sentences)
        for sentence in sentences:
            st.session_state.messages.append({"role": "🐱", "content": sentence})
            chat_title.title("正在输入……")

            time.sleep((random.random()*0.1+0.1)*float(len(sentence)))
            with st.chat_message("🐱"):
                st.markdown(sentence)
            chat_title.title("MiaoMiao")
            time.sleep(0.1)

if st.sidebar.button("Logout"):
    st.session_state.messages = []
    st.switch_page("login.py")

