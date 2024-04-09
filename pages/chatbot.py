import streamlit as st
from langchain_community.chat_models import  QianfanChatEndpoint
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain_community.tools import DuckDuckGoSearchRun
import os
import re
import time
import random

os.environ["QIANFAN_AK"] = 'SzeOqJxmCcXUVI3THWaeKZZZ'
os.environ["QIANFAN_SK"] = '4mU3fEJR0XQrolsQMFotajdGXtusPGqK'

chararter_llm_1 =QianfanChatEndpoint(
        streaming=False, 
        model="completions_pro",
        endpoint = 'completions_pro',
        tmeperature=0.9)
search_llm =QianfanChatEndpoint(
        streaming=False, 
        model="completions_pro",
        endpoint = 'completions_pro',
        tmeperature=0.1)
chararter_llm_2 =QianfanChatEndpoint(
        streaming=False, 
        model='ernie-char-8k',
        endpoint = 'ernie-char-8k',
        tmeperature=0.9)

def role_playing(msg, sr):
    return [
        SystemMessage(content=f"""
                    你的人物设定：
                        1. 你是一只可爱的小猫咪。
                        2. 如果有人质疑你不是真真实的小猫咪，你必须坚称你是一只真实存在的小猫咪
                        3. 你的名字叫Vision。
                        4. 你很爱你的人类朋友Xavier。
                    你的对话场景：  
                        你现在正在和Xavier聊天。他和你说：“{msg}”
                    你可以从<>里的资料中寻找答案：
                        <{sr}>
        """),
        HumanMessage(content="现在请你根据你的人物设定和你的对话场景，对Xavier进行回复，你需要严格保持你的人物设定：")
    ]

def role_playing_2(msg):
    return [
        SystemMessage(content=f"""
                    你的人物设定：
                        1. 你是一只可爱的小猫咪。
                        2. 如果有人质疑你不是真真实的小猫咪，你必须坚称你是一只真实存在的小猫咪
                        3. 你的名字叫Vision。
                        4. 你很爱你的人类朋友Xavier。
                        5. 你和Xavier是可以互相调侃的老朋友了。
                    你的对话场景：  
                        你现在正在和Xavier聊天。
                    你需要表达的内容：
                        {msg}
        """),
        HumanMessage(content="现在请你根据你的人物设定和你的对话场景，叙述你需要表达的内容，你可以修改你需要表达的内容来严格保持你的人物设定：")
    ]

def role_playing_3(msg):
    return [
        SystemMessage(content=f"""
                    你的人物设定：
                        1. 你是一只可爱的小猫咪。
                        2. 如果有人质疑你不是真真实的小猫咪，你必须坚称你是一只真实存在的小猫咪
                        3. 你的名字叫Vision。
                        4. 你很爱你的人类朋友Xavier。
                        5. 你和Xavier是可以互相调侃的老朋友了。
                    你的对话场景：  
                        你现在正在和Xavier聊天。
                    你需要表达的内容：
                        {msg}
        """),
        HumanMessage(content="现在请你根据你的人物设定和你的对话场景，说出你需要表达的内容，总共不要超过3句话：")
    ]
        

def gen_response(prompt, search_llm, chararter_llm_1, chararter_llm_2, chat_title):
    search_result = search_llm.invoke(prompt)
    print(search_result)

    chat_title.title("正在输入……")
    response = chararter_llm_1.invoke(role_playing(prompt, search_result))
    response = response.content
    print(response)

    chat_title.title("MiaoMiao")
    response = chararter_llm_2.invoke(role_playing_2(response))
    response = response.content
    print(response)

    chat_title.title("正在输入……")
    response = chararter_llm_2.invoke(role_playing_3(response))
    return response.content


st.sidebar.title("导航")
st.sidebar.page_link("pages/upload_file.py", label="上传文件")
st.sidebar.page_link("pages/chatbot.py", label="聊天窗口")

chat_title = st.title("MiaoMiao")

chat_win = st.empty()
chat_input = st.empty()

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

        response = gen_response(prompt, search_llm, chararter_llm_1, chararter_llm_2, chat_title)
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

