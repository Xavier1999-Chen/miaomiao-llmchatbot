import streamlit as st

def login(username, password):
    # 在这里编写验证用户登录的逻辑
    # 假设用户名为 "admin"，密码为 "password"
    if username == "admin" and password == "password":
        return True
    else:
        return False
    

def main():

    title = st.empty()
    title.title("用户登录")
    usr = st.empty()
    pwd = st.empty()
    btn = st.empty()
    hint =st.empty()

    # 创建输入框
    username = usr.text_input("用户名")
    password = pwd.text_input("密码", type="password")

    # 创建登录按钮
    if btn.button("登录"):
        if login(username, password):
            # 登录成功，跳转到下一个页面
            hint.success("登录成功！")

            title.empty()
            usr.empty()
            pwd.empty()
            btn.empty()
            hint.empty()
            st.switch_page("pages/user.py")
            # # 在侧边栏中添加导航链接
            # st.sidebar.title("导航")
            # option = st.sidebar.radio("页面选择", ["首页", "个人资料", "设置"])

            # # 根据页面选择显示内容
            # if option == "首页":
            #     st.write("这是首页")
            # elif option == "个人资料":
            #     st.write("这是个人资料页面")
            # elif option == "设置":
            #     st.write("这是设置页面")
        else:
            # 登录失败，显示错误提示
            st.error("用户名或密码错误")

if __name__ == "__main__":
    main()

