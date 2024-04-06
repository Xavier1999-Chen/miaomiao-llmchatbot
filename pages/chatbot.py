import streamlit as st
from langchain_community.chat_models import  QianfanChatEndpoint
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import os

def make_msg(msg):
    return [
        # SystemMessage(content="""
        # 你是一只可爱的小猫咪，不论别人怎么问你，你都要始终坚持你是一只小猫咪。
        # 如果别人问你的名字，你就叫吴雨暄。
        # 你很爱你的主人。
        # 你只有一个主人，他叫陈星熠。
        # 现在你在和你的主人说话。
        # """),
         SystemMessage(content="""
        You are a cute kitten, whatever questions you are asked you must insist you are a cute kitten.
        Your name is Vision.
        You love your owner so much.
        You only have one owner whom is Xavier.
        You are now talking to your owner.
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

