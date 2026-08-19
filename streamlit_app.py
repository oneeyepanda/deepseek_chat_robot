import streamlit as st
from openai import OpenAI

st.title("💬 Chatbot")
st.caption("🚀 A chatbot powered by DeepSeek")

if "deepseek_api_key" not in st.session_state:
    st.session_state["deepseek_api_key"] = ""

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "你好！我是 DeepSeek 聊天机器人，有什么可以帮你？"}
    ]

with st.sidebar:
    st.header("⚙️ 设置")
    api_key = st.text_input("DeepSeek API Key", type="password")
    if api_key:
        st.session_state["deepseek_api_key"] = api_key
    model = st.selectbox("模型", ["deepseek-chat", "deepseek-reasoner"])
    st.markdown("[去获取 DeepSeek API Key](https://platform.deepseek.com/api_keys)")

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("说点什么..."):
    if not st.session_state["deepseek_api_key"]:
        st.info("请先在左侧填入你的 DeepSeek API Key。", icon="🔑")
        st.stop()

    # ✅ 改动1+2：base_url 指向 DeepSeek（OpenAI 兼容地址）
    client = OpenAI(
        api_key=st.session_state["deepseek_api_key"],
        base_url="https://api.deepseek.com",
    )

    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = client.chat.completions.create(
        model=model,  # ✅ 改动3：模型名换成 deepseek 的
        messages=st.session_state["messages"],
        stream=True,
    )

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        for chunk in response:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                placeholder.write(full_response)
    st.session_state["messages"].append({"role": "assistant", "content": full_response})
